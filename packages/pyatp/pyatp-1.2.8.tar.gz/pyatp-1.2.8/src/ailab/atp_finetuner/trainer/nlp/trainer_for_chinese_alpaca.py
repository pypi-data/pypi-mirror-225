from typing import Callable
import math
import os
from transformers import TrainingArguments, Trainer
from peft import get_peft_model_state_dict
from ailab.atp_dataset.dataset import AILabDataset
from ailab.atp_finetuner.trainer import AILabTrainer 
from ailab.atp_finetuner.model import AILabModel
from ailab.atp_finetuner.datacollator import AILabDataCollator
from ailab.atp_finetuner.metric import AILabMetric
from ailab.atp_finetuner.preprossor import AILabPreprocessor
from ailab.atp_finetuner.build import TrainerRg
from ailab.atp_finetuner.constant import Task, Model
from ailab.utils.callbacks import TrainProgress

@TrainerRg.register((Task.question_answering, Model.chinese_alpaca))
class ChineseAlpacaTrainer(AILabTrainer):
    def __init__(self):
        super().__init__()

    def preprocess(self, dataset:AILabDataset, model:AILabModel, preprocessor: AILabPreprocessor, \
                      data_collator:AILabDataCollator, metric:AILabMetric, train_progress:Callable, **kwargs):
        train_args = kwargs['train_args']
        output_dir = train_args.get('output_dir', 'my_model')
        learning_rate = train_args.get('learning_rate', 1e-5)
        num_train_epochs = train_args.get('num_train_epochs', 2)
        evaluation_strategy = train_args.get('evaluation_strategy', "epoch")
        save_strategy = train_args.get('save_strategy', "steps")
        per_device_train_batch_size = train_args.get('per_device_train_batch_size', 4)
        gradient_accumulation_steps = train_args.get('gradient_accumulation_steps', 1)
        logging_steps = train_args.get('logging_steps', 10)
        warmup_steps = train_args.get('warmup_steps', 0)
        fp16 = train_args.get('fp16', True)
        bf16 = train_args.get('bf16', False)
        eval_steps = train_args.get('eval_steps', 250)
        save_steps = train_args.get('save_steps', 500)
        resume_from_checkpoint = train_args.get('resume_from_checkpoint', False)

        deepspeed_dir = os.path.dirname(os.path.abspath(__file__))
        deepspeed_dir = os.path.join(deepspeed_dir,"ds_zero2_no_offload.json")
        training_args=TrainingArguments(
            per_device_train_batch_size=per_device_train_batch_size,
            per_device_eval_batch_size=4,
            gradient_accumulation_steps=gradient_accumulation_steps,
            lr_scheduler_type="cosine",
            warmup_ratio=0.03,
            warmup_steps=0,
            weight_decay=0.0,
            learning_rate=learning_rate,
            fp16=fp16,
            bf16=bf16,
            logging_steps=logging_steps,
            evaluation_strategy=evaluation_strategy,
            save_strategy=save_strategy,
            eval_steps=eval_steps,
            save_steps=save_steps,
            output_dir=output_dir,
            save_total_limit=3,
            load_best_model_at_end=False,
            group_by_length=False,
            report_to= None,
            run_name= None,
            push_to_hub=False,
            num_train_epochs=num_train_epochs,
            ddp_find_unused_parameters=False,
            ddp_timeout=30000,
            deepspeed=deepspeed_dir,
            do_train=True,
            gradient_checkpointing=True,
            greater_is_better=None,
        )

        print(f'ChineseAlpacaTrainer training_args {training_args}')

        model = model.model_ins
        tokenizer = preprocessor.preprocessor_ins
        embedding_size = model.get_input_embeddings().weight.shape[0]
        if len(tokenizer) != embedding_size:
            print("resize the embedding size by the size of the tokenizer")
            model.resize_token_embeddings(len(tokenizer))

        lora_rank=8
        lora_alpha=32
        lora_trainable="q_proj,v_proj,k_proj,o_proj,gate_proj,down_proj,up_proj"
        modules_to_save="embed_tokens,lm_head"
        lora_dropout=0.05

        from peft import LoraConfig, TaskType, get_peft_model
        target_modules = lora_trainable.split(',')
        modules_to_save = modules_to_save.split(',')
        peft_config = LoraConfig(
            task_type=TaskType.CAUSAL_LM, 
            target_modules=target_modules,
            inference_mode=False, 
            r=lora_rank, lora_alpha=lora_alpha, 
            lora_dropout=lora_dropout,
            modules_to_save=modules_to_save)
        model = get_peft_model(model, peft_config)

        #model.base_model.tie_weights()
        model.print_trainable_parameters()
        print(f"model.modules_to_save: {model.modules_to_save}")
        old_state_dict = model.state_dict
        model.state_dict = (
            lambda self, *_, **__: get_peft_model_state_dict(self, old_state_dict())
        ).__get__(model, type(model))

        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=dataset.to_hf_dataset()["train"],
            eval_dataset=dataset.to_hf_dataset()["test"],
            data_collator=data_collator.datacollator_ins,
            callbacks=[TrainProgress(train_progress)],
        )

        self.trainer = trainer
        self.model = model
        self.tokenizer = tokenizer
        self.output_dir = output_dir
        self.resume_from_checkpoint = resume_from_checkpoint
    
    def train(self):
        model = self.model
        tokenizer = self.tokenizer
        trainer = self.trainer
        output_dir = self.output_dir 
        resume_from_checkpoint = self.resume_from_checkpoint

        train_result = trainer.train(resume_from_checkpoint=resume_from_checkpoint)
        trainer.save_model()  # Saves the tokenizer too for easy upload

        metrics = train_result.metrics
        metrics["train_samples"] = len(trainer.train_dataset)
        trainer.log_metrics("train", metrics)
        trainer.save_metrics("train", metrics)
        trainer.save_state()

        import torch.distributed as dist
        if dist.get_rank() == 0:
            import shutil
            from transformers.modeling_utils import unwrap_model
            try:
                unwrap_model(model).peft_config.save_pretrained(output_dir)
            except AttributeError:
                unwrap_model(model).peft_config['default'].save_pretrained(output_dir)
            shutil.move(
                os.path.join(output_dir,'pytorch_model.bin'),
                os.path.join(output_dir,'adapter_model.bin'))
            tokenizer.save_pretrained(output_dir)

        print("*** Evaluate ***")
        metrics = trainer.evaluate()
        metrics["eval_samples"] =len(trainer.eval_dataset)
        try:
            perplexity = math.exp(metrics["eval_loss"])
        except OverflowError:
            perplexity = float("inf")
        metrics["perplexity"] = perplexity

        trainer.log_metrics("eval", metrics)
        trainer.save_metrics("eval", metrics)

    def postprocess(self):
        self.trainer.evaluate()



