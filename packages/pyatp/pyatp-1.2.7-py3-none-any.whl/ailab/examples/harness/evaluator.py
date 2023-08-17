import os
from ailab.atp_evaluation.constant import BenchMarkType
from ailab.atp_evaluation.evaluator import AILabEvaluator

# 测试数据集本地路径
DATASET_DIR:str = "/data1/cgzhang6/eval_datasets"
OUTDIR:str = "./result"

class TaskType(object):
    arc_challenge = "arc_challenge"
    hellaswag = "hellaswag"
    mmlu = "hendrycksTest-*"
    truthfulqa_mc = "truthfulqa_mc"

class ModelName(object):
    stanford_alpaca = 'stanford_alpaca'
    vicuna = 'chinese_llama_vicuna'
    chinese_alpaca = 'chinese_llama_alpaca'
    chatglm_6b = 'chatglm_6b'
    chatglm2_6b = 'chatglm2_6b'
    baichuan_7b = 'baichuan_7b'
    open_llama = 'open_llama'
    baichuan_13b = 'baichuan_13b'
    bloomz_7b1_mt = 'bloomz-7b1-mt'
    falcon_7b = 'falcon-7b'
    moss_moon_003_base = 'moss_moon_003_base'
    llama2_7b = 'llama2_7b'

def get_args(model_name:ModelName, tasktype:TaskType, model_args:str,
             model_type:str = "hf-causal-experimental",
             peft:str = None,
             use_accelerate:bool = False,
             num_fewshot:int = 0,
             data_dir:str = DATASET_DIR,
             gpu_index:int = 0):
    if model_name == ModelName.chatglm_6b or model_name == ModelName.chatglm2_6b:
        model_type = "hf-chatglm"
    if use_accelerate:
        model_args = f"{model_args},use_accelerate=True"
    else:
        model_args = f"{model_args},use_accelerate=False"
    if tasktype == TaskType.arc_challenge:
        num_fewshot = 25
    elif tasktype == TaskType.hellaswag:
        num_fewshot = 10
    elif tasktype == TaskType.mmlu:
        num_fewshot = 5
    task_name = tasktype
    if tasktype == TaskType.mmlu:
        task_name = "mmlu"
    outfile = f"{model_name}_{task_name}_{num_fewshot}s.json"
    if peft is not None:
        model_args = f"{model_args},peft={peft}"
        outfile = f"{model_name}_peft_{task_name}_{num_fewshot}s.json"

    output_path = os.path.join(OUTDIR, outfile)

    args = {
        "harness_args": {
            "model": model_type,
            "model_args": model_args,
            "tasks": tasktype,
            "num_fewshot": num_fewshot,
            "batch_size": 16,
            "no_cache": True,
            "data_dir": data_dir,
            "output_path": output_path,
            "device": f"cuda:{gpu_index}",
        },
    }
    print(args)
    return args

def stanford_alpaca_test(tasktype:TaskType, use_peft:bool = False, gpu_index:int = 0):
    # (原始模型 - hellaswag - 1:51:27 - A800 多卡)
    # (原始模型 - truthfulqa_mc - 02:59 - A800 多卡)
    # (原始模型 - truthfulqa_mc - 02:38 - A800 单卡)
    # (原始模型 - truthfulqa_mc - 04:18 - A800 多卡 - 设置use_fast为False加载tokenizer)
    lora_weight="/data1/cgzhang6/finetuned_models/my_standford_alpaca_model"
    model_args = "pretrained='/home/sdk_models/llama-7b-hf',load_in_8bit=True,dtype='float16',tokenizer='/data1/cgzhang6/tokenizer/llama-7b-hf_tokenizer'"
    args = get_args(ModelName.stanford_alpaca, 
                    tasktype, 
                    model_args,
                    peft=lora_weight if use_peft else None,
                    use_accelerate = False,
                    gpu_index = gpu_index)
    evaluator = AILabEvaluator(BenchMarkType.harness, **args)
    evaluator.evaluate()

def vicuna_test(tasktype:TaskType, use_peft:bool = False, gpu_index:int = 0):
    lora_weight="/data1/cgzhang6/finetuned_models/my_chinese_llama_vicuna_model"
    model_args = "pretrained='/home/sdk_models/llama-7b-hf',load_in_8bit=True,dtype='float16',tokenizer='/data1/cgzhang6/tokenizer/chinese_llama_vicuna_tokenizer'"
    args = get_args(ModelName.vicuna, 
                    tasktype, 
                    model_args,
                    peft=lora_weight if use_peft else None,
                    use_accelerate = False,
                    gpu_index = gpu_index)
    evaluator = AILabEvaluator(BenchMarkType.harness, **args)
    evaluator.evaluate()

def chinese_alpaca_test(tasktype:TaskType, use_peft:bool = False, gpu_index:int = 0):
    lora_weight="/data1/cgzhang6/finetuned_models/my_chinese_llama_alpaca_model"
    model_args = "pretrained='/home/sdk_models/llama-7b-hf',load_in_8bit=True,dtype='float16',tokenizer='/data1/cgzhang6/tokenizer/chinese_llama_alpaca_tokenizer'"
    args = get_args(ModelName.chinese_alpaca, 
                    tasktype, 
                    model_args,
                    peft=lora_weight if use_peft else None,
                    use_accelerate = False,
                    gpu_index = gpu_index)
    evaluator = AILabEvaluator(BenchMarkType.harness, **args)
    evaluator.evaluate()

def chatglm_6b_test(tasktype:TaskType, use_peft:bool = False, gpu_index:int = 0):
    #  (原始模型 - arc_challenge - 24:50 - A800 多卡)
    # TODO: lora权重加载目前会报错，待新的lora模型上传后验证
    # add_special_tokens为False时，推理会报错
    lora_weight="/data1/cgzhang6/finetuned_models/my_chatglm_6b_model"
    model_args = "pretrained='/data1/cgzhang6/models/chatglm-6b',add_special_tokens=True,trust_remote_code=True,dtype='float16'"
    args = get_args(ModelName.chatglm_6b, 
                    tasktype, 
                    model_args,
                    peft=lora_weight if use_peft else None,
                    gpu_index = gpu_index)
    evaluator = AILabEvaluator(BenchMarkType.harness, **args)
    evaluator.evaluate()

def chatglm2_6b_test(tasktype:TaskType, use_peft:bool = False, gpu_index:int = 0):
    # (原始模型 - arc_challenge - 14:56 - A800 多卡)
    lora_weight="/data1/cgzhang6/finetuned_models/my_chatglm2_model/checkpoint-100"
    model_args = "pretrained='/home/sdk_models/chatglm2_6b',add_special_tokens=True,trust_remote_code=True,dtype='float16'"
    args = get_args(ModelName.chatglm2_6b, 
                    tasktype, 
                    model_args,
                    peft=lora_weight if use_peft else None,
                    gpu_index = gpu_index)
    evaluator = AILabEvaluator(BenchMarkType.harness, **args)
    evaluator.evaluate()

def baichuan_7b_test(tasktype:TaskType, use_peft:bool = False, gpu_index:int = 0):
    lora_weight="/data1/cgzhang6/finetuned_models/my_baichuan_model"
    model_args = "pretrained='/home/sdk_models/baichuan_7b',trust_remote_code=True"
    args = get_args(ModelName.baichuan_7b, 
                    tasktype, 
                    model_args,
                    peft=lora_weight if use_peft else None,
                    gpu_index = gpu_index)
    evaluator = AILabEvaluator(BenchMarkType.harness, **args)
    evaluator.evaluate()

def open_llama_test(tasktype:TaskType, use_peft:bool = False, gpu_index:int = 0):
    # (原始模型 - mmlu - 1:47:11 - A800 单卡)
    lora_weight="/data1/cgzhang6/finetuned_models/my_open_llama_model"
    model_args = "pretrained='/data1/cgzhang6/models/open_llama_7b',trust_remote_code=True"
    args = get_args(ModelName.open_llama, 
                    tasktype, 
                    model_args,
                    peft=lora_weight if use_peft else None,
                    gpu_index = gpu_index)
    evaluator = AILabEvaluator(BenchMarkType.harness, **args)
    evaluator.evaluate()

def baichuan_13b_test(tasktype:TaskType, use_peft:bool = False, gpu_index:int = 0):
    lora_weight="/data1/cgzhang6/finetuned_models/my_baichuan13b_model"
    model_args = "pretrained='/data1/cgzhang6/models/Baichuan-13B-Base',trust_remote_code=True"
    args = get_args(ModelName.baichuan_13b, 
                    tasktype, 
                    model_args,
                    peft=lora_weight if use_peft else None,
                    gpu_index = gpu_index)
    evaluator = AILabEvaluator(BenchMarkType.harness, **args)
    evaluator.evaluate()

def bloomz_7b1_mt_test(tasktype:TaskType, use_peft:bool = False, gpu_index:int = 0):
    lora_weight="/data1/cgzhang6/finetuned_models/my_bloomz_model"
    model_args = "pretrained='/data1/cgzhang6/models/bloomz-7b1-mt',trust_remote_code=True"
    args = get_args(ModelName.bloomz_7b1_mt, 
                    tasktype, 
                    model_args,
                    peft=lora_weight if use_peft else None,
                    gpu_index = gpu_index)
    evaluator = AILabEvaluator(BenchMarkType.harness, **args)
    evaluator.evaluate()

def falcon_7b_test(tasktype:TaskType, use_peft:bool = False, gpu_index:int = 0):
    # (原始模型 - arc_challenge - 25:20 - A800 多卡)
    lora_weight="/data1/cgzhang6/finetuned_models/my_falcon_model"
    model_args = "pretrained='/data1/cgzhang6/models/falcon-7b',trust_remote_code=True"
    args = get_args(ModelName.falcon_7b, 
                    tasktype, 
                    model_args,
                    peft=lora_weight if use_peft else None,
                    gpu_index = gpu_index)
    evaluator = AILabEvaluator(BenchMarkType.harness, **args)
    evaluator.evaluate()

def moss_moon_003_base_test(tasktype:TaskType, use_peft:bool = False, gpu_index:int = 0):
    # (原始模型 - arc_challenge - 34:39 - A800 多卡)
    lora_weight="/data1/cgzhang6/finetuned_models/my_moss_model"
    model_args = "pretrained='/data1/cgzhang6/models/moss-moon-003-base',trust_remote_code=True"
    args = get_args(ModelName.moss_moon_003_base, 
                    tasktype, 
                    model_args,
                    peft=lora_weight if use_peft else None,
                    gpu_index = gpu_index)
    evaluator = AILabEvaluator(BenchMarkType.harness, **args)
    evaluator.evaluate()

def llama2_7b_test(tasktype:TaskType, use_peft:bool = False, gpu_index:int = 0):
    # (原始模型 - arc_challenge - 14:40 - A800 多卡)
    # TODO: 暂无测试权重
    lora_weight="/data1/cgzhang6/finetuned_models/my_llama2_7b_model"
    model_args = "pretrained='/data1/cgzhang6/models/llama2-7b-hf',trust_remote_code=True"
    args = get_args(ModelName.llama2_7b, 
                    tasktype, 
                    model_args,
                    peft=lora_weight if use_peft else None,
                    gpu_index = gpu_index)
    evaluator = AILabEvaluator(BenchMarkType.harness, **args)
    evaluator.evaluate()

if __name__ == '__main__':
    chatglm2_6b_test(tasktype = TaskType.mmlu, use_peft = False, gpu_index = 7)


 

