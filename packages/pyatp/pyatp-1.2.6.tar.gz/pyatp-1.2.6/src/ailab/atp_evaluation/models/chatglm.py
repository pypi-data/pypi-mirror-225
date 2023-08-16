import os
import numpy as np
import torch
from ailab.atp_evaluation.models.base import AILabModel
from transformers.models import auto
from transformers import AutoConfig
from ailab.atp_evaluation.build import ModelRg
from ailab.atp_evaluation.constant import Task, Model
from transformers import GenerationConfig
from transformers.generation.logits_process import LogitsProcessor
from transformers.generation.utils import LogitsProcessorList
from peft import LoraConfig, TaskType, get_peft_model
from ailab.log import logger

class InvalidScoreLogitsProcessor(LogitsProcessor):
    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor) -> torch.FloatTensor:
        if torch.isnan(scores).any() or torch.isinf(scores).any():
            scores.zero_()
            scores[..., 5] = 5e4
        return scores

@ModelRg.register((Task.question_answering, Model.chatglm_6b))
class ChatGlmModel(AILabModel):
    def __init__(self, model_name: str, model: any, tokenizer: any) -> None:
        super().__init__(model_name, model, tokenizer)
    
    @classmethod
    def build_model(cls, device_name:str, model_name:str, model_dir:str, lora_weight_dir: str, tokenizer_dir: str, **kwargs):
        model_name_or_dir = model_name if model_dir is None else model_dir
        model = auto.AutoModel.from_pretrained(model_name_or_dir, load_in_8bit=True, torch_dtype=torch.float16, trust_remote_code=True, device_map="auto")
        if lora_weight_dir is not None:
            logger.info(f"use finetuned chatglm model, lora weight: {lora_weight_dir}")
            lora_weight_bin = os.path.join(lora_weight_dir, "adapter_model.bin")
            peft_config = LoraConfig(
                task_type=TaskType.CAUSAL_LM,
                inference_mode=True,
                r=8,
                lora_alpha=32,
                lora_dropout=0.1)
            model = get_peft_model(model, peft_config)
            model.load_state_dict(torch.load(lora_weight_bin), strict=False)
        else:
            logger.info("use base chatglm model")
        pc_name_dir = model_name if tokenizer_dir is None else tokenizer_dir
        tokenizer = auto.AutoTokenizer.from_pretrained(pc_name_dir, use_fast=False, add_bos_token=False, trust_remote_code=True)
        model.eval()
        config = AutoConfig.from_pretrained(pc_name_dir, trust_remote_code=True, device_map='auto')
        return cls(model_name, model, tokenizer)

    def get_answer_of_multiple_choices_question(self, prompt, do_sample=False, num_beams=1, top_p=0.7, temperature=0.95, logits_processor=None, **kwargs):
        #return self.__get_answer_of_multiple_choices_question1(prompt, do_sample, num_beams, top_p, temperature, logits_processor, kwargs)
        return self.__get_answer_of_multiple_choices_question2(prompt)

    # 方法1 速度较慢 新机器耗时 mmlu:11h52m  
    def __get_answer_of_multiple_choices_question1(self, prompt, do_sample=False, num_beams=1, top_p=0.7, temperature=0.95, logits_processor=None, **kwargs):
        if logits_processor is None:
            logits_processor = LogitsProcessorList()
        logits_processor.append(InvalidScoreLogitsProcessor())

        generation_config = GenerationConfig(
            temperature=temperature,
            top_p=top_p,
            top_k=40,
            do_sample=do_sample,
            num_beams=num_beams,
            max_new_tokens=128,
            logits_processor=logits_processor,
            **kwargs,
        )
        with torch.no_grad():
            inputs = self._tokenizer([prompt], return_tensors="pt")
            inputs = inputs.to(self._model.device)
            outputs = self._model.generate(**inputs, generation_config=generation_config, return_dict_in_generate=True, output_scores=True)
            score = outputs.scores[0][0].tolist()
            choice_score = [
                score[self._tokenizer("A").input_ids[0]], 
                score[self._tokenizer("B").input_ids[0]],
                score[self._tokenizer("C").input_ids[0]],
                score[self._tokenizer("D").input_ids[0]]
            ]
            # logger.info(choice_score)
            ranked_index = [index for index, value in sorted(list(enumerate(choice_score)), key=lambda x:x[1], reverse=True)]
            return self._choices[ranked_index[0]]

    ## 方法2 速度较快 新机器 mmlu:32m ceval:28m
    def __get_answer_of_multiple_choices_question2(self, prompt):
        input_ids = self._tokenizer(prompt, return_tensors="pt").input_ids.cuda()
        logits = self._model(
             input_ids=input_ids,
        ).logits[:,-1].flatten()

        probs = (
            torch.nn.functional.softmax(
                torch.tensor(
                    [
                        logits[self._tokenizer("A").input_ids[0]],
                        logits[self._tokenizer("B").input_ids[0]],
                        logits[self._tokenizer("C").input_ids[0]],
                        logits[self._tokenizer("D").input_ids[0]],
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
        # logger.info(probs)
        return self._choices[np.argmax(probs)]