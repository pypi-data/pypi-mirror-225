import os
from typing import Callable
import torch
from transformers import TrainingArguments, Trainer
from peft import get_peft_model_state_dict, set_peft_model_state_dict
from ailab.atp_dataset.dataset import AILabDataset
from ailab.atp_finetuner.trainer import AILabTrainer 
from ailab.atp_finetuner.model import AILabModel
from ailab.atp_finetuner.datacollator import AILabDataCollator
from ailab.atp_finetuner.metric import AILabMetric
from ailab.atp_finetuner.preprossor import AILabPreprocessor
from ailab.atp_finetuner.build import TrainerRg
from ailab.atp_finetuner.constant import Task, Model
from ailab.utils.callbacks import TrainProgress

@TrainerRg.register((Task.question_answering_cn, Model.vicuna))
@TrainerRg.register((Task.question_answering_cn, Model.open_llama))
class Vicunatrainer(AILabTrainer):
    def __init__(self):
        super().__init__()

    def preprocess(self, dataset:AILabDataset, model:AILabModel, preprocessor: AILabPreprocessor, \
                      data_collator:AILabDataCollator, metric:AILabMetric, train_progress:Callable, **kwargs):
        train_args = kwargs['train_args']
        output_dir = train_args.get('output_dir', 'my_model')
        learning_rate = train_args.get('learning_rate', 1e-5)
        num_train_epochs = train_args.get('num_train_epochs', 2)
        evaluation_strategy = train_args.get('evaluation_strategy', "epoch")
        save_strategy = train_args.get('save_strategy', "epoch")
        per_device_train_batch_size = train_args.get('per_device_train_batch_size', 16)
        gradient_accumulation_steps = train_args.get('gradient_accumulation_steps', 4)
        per_device_eval_batch_size = train_args.get('per_device_eval_batch_size', 16)
        weight_decay = train_args.get('weight_decay', 0.01)
        logging_steps = train_args.get('logging_steps', 10)
        warmup_steps = train_args.get('warmup_steps', 100)
        fp16 = train_args.get('fp16', False)
        bf16 = train_args.get('bf16', True)
        optim = train_args.get('optim', "adamw_torch")
        eval_steps = train_args.get('eval_steps', 200)
        save_steps = train_args.get('save_steps', 200)
        max_steps = train_args.get('max_steps', 5000)
        resume_from_checkpoint = train_args.get('resume_from_checkpoint', False)
        
        deepspeed_dir = os.path.dirname(os.path.abspath(__file__))
        deepspeed_dir = os.path.join(deepspeed_dir,"ds_zero2_no_offload.json")
        training_args = TrainingArguments(
            output_dir=output_dir,
            evaluation_strategy=evaluation_strategy,
            save_strategy=save_strategy,
            learning_rate=learning_rate,
            per_device_train_batch_size=per_device_train_batch_size,
            per_device_eval_batch_size=per_device_eval_batch_size,
            num_train_epochs=num_train_epochs,
            weight_decay=weight_decay,
            gradient_accumulation_steps = gradient_accumulation_steps,
            logging_steps = logging_steps,
            warmup_steps = warmup_steps,
            fp16 = fp16,
            bf16 = bf16,
            optim = optim,
            eval_steps = eval_steps,
            save_steps = save_steps,
            save_total_limit=3,
            load_best_model_at_end=False,
            report_to=[],
            ignore_data_skip=False,
            push_to_hub=False,
            ddp_find_unused_parameters=False,
            ddp_timeout=30000,
            deepspeed=deepspeed_dir,
        )

        print(f'Vicunatrainer training_args {training_args}')

        trainer = Trainer(
            model=model.model_ins,
            args=training_args,
            train_dataset=dataset.to_hf_dataset()["train"],
            eval_dataset=dataset.to_hf_dataset()["test"],
            data_collator=data_collator.datacollator_ins,
            callbacks=[TrainProgress(train_progress)],
        )
        self.trainer = trainer
        self.model = model.model_ins
        self.output_dir = output_dir
        self.resume_from_checkpoint = resume_from_checkpoint

    def train(self):
        model = self.model
        resume_from_checkpoint = self.resume_from_checkpoint

        from transformers.trainer_utils import get_last_checkpoint
        if resume_from_checkpoint:
            resume_from_checkpoint = get_last_checkpoint(self.output_dir)
            if resume_from_checkpoint is None:
                resume_from_checkpoint = False
            else:
                checkpoint_name = os.path.join(resume_from_checkpoint, "pytorch_model.bin")
                if not os.path.exists(checkpoint_name):
                    checkpoint_name = os.path.join(resume_from_checkpoint, "adapter_model.bin")
                if os.path.exists(checkpoint_name):
                    print(f"Restarting from {checkpoint_name}")
                    adapters_weights = torch.load(checkpoint_name)
                    set_peft_model_state_dict(model, adapters_weights)
                else:
                    resume_from_checkpoint = False

        model.config.use_cache = False
        old_state_dict = model.state_dict
        model.state_dict = (
            lambda self, *_, **__: get_peft_model_state_dict(
                self, old_state_dict()
            )
        ).__get__(model, type(model))
        model = torch.compile(model)

        self.trainer.train(resume_from_checkpoint=resume_from_checkpoint)
        model.save_pretrained(self.output_dir)

    def postprocess(self):
        self.trainer.evaluate()



