from typing import List
import numpy as np
import torch
from transformers import LlamaForCausalLM, LlamaTokenizer
from ailab.atp_evaluation.models.base import AILabModel
from ailab.atp_evaluation.build import ModelRg
from ailab.atp_evaluation.constant import Task, Model
from ailab.log import logger

@ModelRg.register((Task.question_answering, Model.vicuna))
@ModelRg.register((Task.question_answering, Model.chinese_alpaca))
@ModelRg.register((Task.question_answering, Model.alpaca))
@ModelRg.register((Task.question_answering, Model.llama_7b))
class LlamaBasedModel(AILabModel):
    def __init__(self, model_name: str, model: any, tokenizer: any) -> None:
        super().__init__(model_name, model, tokenizer)
    
    @classmethod
    def build_model(cls, device_name:str, model_name:str, model_dir:str, lora_weight_dir: str, tokenizer_dir: str, **kwargs):
        model_name_or_dir = model_name if model_dir is None else model_dir
        model = LlamaForCausalLM.from_pretrained(model_name_or_dir, load_in_8bit=True, torch_dtype=torch.float16, device_map="auto")
        pc_name_dir = model_name if tokenizer_dir is None else tokenizer_dir
        tokenizer = LlamaTokenizer.from_pretrained(pc_name_dir)
        if lora_weight_dir is not None:
            if model_name is Model.vicuna:
                logger.info(f"use chinese vicuna lora weight model {lora_weight_dir}")
                from ailab.utils.streampeft import StreamPeftGenerationMixin
                model = StreamPeftGenerationMixin.from_pretrained(model, lora_weight_dir, torch_dtype=torch.float16, device_map="auto")
            elif model_name is Model.alpaca:
                logger.info(f"use alpaca lora weight model {lora_weight_dir}")
                from peft import PeftModel
                model = PeftModel.from_pretrained(model, lora_weight_dir, torch_dtype=torch.float16, device_map="auto")
                model.config.pad_token_id = tokenizer.pad_token_id = 0  # unk
                model.config.bos_token_id = 1
                model.config.eos_token_id = 2
            elif model_name is Model.chinese_alpaca:
                logger.info(f"use chinese alpaca lora weight model {lora_weight_dir}")
                from peft import PeftModel
                model_vocab_size = model.get_input_embeddings().weight.size(0)
                tokenzier_vocab_size = len(tokenizer)
                logger.info(f"Vocab of the base model: {model_vocab_size}")
                logger.info(f"Vocab of the tokenizer: {tokenzier_vocab_size}")
                if model_vocab_size != tokenzier_vocab_size:
                    assert tokenzier_vocab_size > model_vocab_size
                    logger.info("Resize model embeddings to fit tokenizer")
                    model.resize_token_embeddings(tokenzier_vocab_size)
                model = PeftModel.from_pretrained(model, lora_weight_dir, torch_dtype=torch.float16, device_map='auto')
            else:
                raise TypeError(f"use unsupported model {lora_weight_dir}")
        else:
            logger.info("use base llama model")
        model.eval()
        return cls(model_name, model, tokenizer)

    def get_answer_of_multiple_choices_question(self, prompt, do_sample=False, num_beams=1, top_p=0.7, temperature=0.95, logits_processor=None, **kwargs):
        input_ids = self._tokenizer(prompt, return_tensors="pt").input_ids.cuda()
        logits = self._model(
             input_ids=input_ids,
        ).logits[:,-1].flatten()

        probs = (
            torch.nn.functional.softmax(
                torch.tensor(
                    [
                        logits[self._tokenizer("A").input_ids[-1]],
                        logits[self._tokenizer("B").input_ids[-1]],
                        logits[self._tokenizer("C").input_ids[-1]],
                        logits[self._tokenizer("D").input_ids[-1]],
                    ],
                    dtype=torch.float32,
                ),
                dim=0,
            )
            .detach()
            .cpu()
            .to(torch.float32)
            .numpy()
        )
        return self._choices[np.argmax(probs)]