import torch
from ailab.atp_finetuner.preprossor import AILabPreprocessor
from ailab.atp_dataset.dataset import AILabDataset
from transformers import LlamaTokenizer
from ailab.atp_finetuner.build import PreProcessorRg
from ailab.atp_finetuner.constant import Task, Model


@PreProcessorRg.register((Task.question_answering, Model.chinese_alpaca))
class ChineseAlpacaPreProcessor(AILabPreprocessor):
    def __init__(self, dataset, preprocessor):
        super().__init__(dataset, preprocessor)

    @classmethod
    def build_preprocessor(cls, model_name:str, dataset: AILabDataset, pc_dir:str, **kwargs):
        pc_name_dir = model_name if pc_dir is None else pc_dir
        tokenizer = LlamaTokenizer.from_pretrained(pc_name_dir, legacy=False)
        return cls(dataset, tokenizer)

    def process_data(self) ->AILabDataset:
        tokenizer = self._preprocessor
        dataset = self._dataset.to_hf_dataset()

        def buid_instruction_dataset(max_seq_length: int, preprocessing_num_workers = None,):
            from datasets import concatenate_datasets
            PROMPT_TEMPLATE = (
                "Below is an instruction that describes a task. "
                "Write a response that appropriately completes the request.\n\n"
                "### Instruction:\n{instruction}\n\n### Response: "
            )
            IGNORE_INDEX = -100

            def tokenization(examples):
                sources = []
                targets = []
                prompt = PROMPT_TEMPLATE
                for instruction, input, output in zip(examples['instruction'],examples['input'],examples['output']):
                    if input is not None and input !="":
                        instruction = instruction+'\n'+input
                    source = prompt.format_map({'instruction':instruction})
                    target = f"{output}{tokenizer.eos_token}"

                    sources.append(source)
                    targets.append(target)

                tokenized_sources = tokenizer(sources,return_attention_mask=False)
                tokenized_targets = tokenizer(targets,return_attention_mask=False,add_special_tokens=False)

                all_input_ids = []
                all_labels = []
                for s,t in zip(tokenized_sources['input_ids'],tokenized_targets['input_ids']):
                    input_ids = torch.LongTensor(s + t)[:max_seq_length]
                    labels = torch.LongTensor([IGNORE_INDEX] * len(s) + t)[:max_seq_length]
                    assert len(input_ids) == len(labels)
                    all_input_ids.append(input_ids)
                    all_labels.append(labels)

                results = {'input_ids':all_input_ids, 'labels': all_labels}
                return results

            all_datasets = []
            tokenization_func = tokenization
            tokenized_dataset = dataset.map(
                tokenization_func,
                batched=True,
                num_proc=preprocessing_num_workers,
                remove_columns=["instruction","input","output"],
                keep_in_memory=False,
                desc="preprocessing on dataset",
            )
            processed_dataset = tokenized_dataset
            processed_dataset.set_format('torch')
            all_datasets.append(processed_dataset['train'])
            all_datasets = concatenate_datasets(all_datasets)
            return processed_dataset

        max_seq_length = 512
        preprocessing_num_workers = 8
        tokenized_dataset = buid_instruction_dataset(max_seq_length,preprocessing_num_workers)
        return AILabDataset(tokenized_dataset)
