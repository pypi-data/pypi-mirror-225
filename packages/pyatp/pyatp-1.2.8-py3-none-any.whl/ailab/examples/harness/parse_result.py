
import argparse
from dataclasses import dataclass
import datetime

import json
import os
from typing import Dict, List, OrderedDict, Tuple
import numpy as np

METRICS = ["acc_norm", "acc_norm", "acc", "mc2"]
BENCHMARKS = ["arc_challenge", "hellaswag", "hendrycksTest", "truthfulqa_mc"]
BENCH_TO_NAME = {
    "arc_challenge": "ARC",
    "hellaswag": "HellaSwag",
    "hendrycksTest": "MMLU",
    "truthfulqa_mc": "TruthfulQA",
}

@dataclass
class EvalResult:
    eval_name: str
    model_args: str
    results: dict

    def to_dict(self):
        data_dict = {}

        data_dict["eval_name"] = self.eval_name # not a column, just a save name
        data_dict["model_args"] = self.model_args
        for benchmark in BENCHMARKS:
            if benchmark not in self.results.keys():
                self.results[benchmark] = None

        for k, v in BENCH_TO_NAME.items():
            data_dict[v] = self.results[k]

        return data_dict

def parse_eval_result(json_filepath: str) -> Tuple[str, list[dict]]:
    with open(json_filepath) as fp:
        data = json.load(fp)

    
    for mmlu_k in ["harness|hendrycksTest-abstract_algebra|5", "hendrycksTest-abstract_algebra"]:
        if mmlu_k in data["versions"] and data["versions"][mmlu_k] == 0:
            return None, [] # we skip models with the wrong version 

    config = data["config"]
    model_args = config.get("model_args", None)

    params_list = model_args.split(',') 
    model_params_dict = {}
    for param in params_list:
        key, value = param.split('=', 1)
        model_params_dict[key.strip()] = value.strip("'")

    # print(model_params_dict)
    pretrained_str = model_params_dict["pretrained"]
    pretrained_model = pretrained_str.split('/')[-1]
    peft_str = model_params_dict.get("peft", None)

    result_key = pretrained_model
    if peft_str is not None:
        peft_name = peft_str.split('/')[-1]
        result_key = f"{pretrained_model}--{peft_name}"

    # print(result_key)
    eval_results = []
    for benchmark, metric in zip(BENCHMARKS, METRICS):
        accs = np.array([v[metric] for k, v in data["results"].items() if benchmark in k])
        if accs.size == 0:
            continue
        mean_acc = np.mean(accs) * 100.0
        eval_results.append(EvalResult(
            eval_name=result_key, model_args=model_args, results={benchmark: mean_acc} 
        ))
    # print(eval_results)
    return result_key, eval_results

def sort_files_by_created_time(files):

    # 获取每个文件元数据中的创建时间
    file_stats = [os.stat(file) for file in files]  
    create_times = [datetime.datetime.fromtimestamp(stat.st_ctime) for stat in file_stats]

    # 按创建时间进行排序
    sorted_paths = [x for _,x in sorted(zip(create_times,files))] 
    
    return sorted_paths

def get_eval_results(dir:str) -> List[EvalResult]:
    json_filepaths = []

    for filename in os.listdir(dir):
        if filename.endswith('.json'):
            json_filepaths.append(os.path.join(dir, filename))
    json_filepaths = sort_files_by_created_time(json_filepaths)

    print("total:", len(json_filepaths), ", list:", json_filepaths)

    eval_results = {}
    for json_filepath in json_filepaths:
        result_key, results = parse_eval_result(json_filepath)
        for eval_result in results:
            if result_key in eval_results.keys():
                # print(result_key)
                # print(eval_result.results)
                eval_results[result_key].results.update(eval_result.results)
                eval_results[result_key].model_args = eval_result.model_args
            else:
                eval_results[result_key] = eval_result

    eval_results = [v for v in eval_results.values()]

    return eval_results


def get_eval_results_dicts(dir:str) -> List[Dict]:
    eval_results = get_eval_results(dir)

    return [e.to_dict() for e in eval_results]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", default="./result")
    args = parser.parse_args()

    r = get_eval_results_dicts(args.dir)
    r.sort(key=lambda x: x["eval_name"])

    print(json.dumps(r, indent=2))