from ailab.atp_evaluation.constant import BenchMarkType
from ailab.atp_evaluation.evaluator import AILabEvaluator

if __name__ == '__main__':
    args = {
        "harness_args": {
            "model": "hf-causal",
            "model_args": "pretrained='/home/sdk_models/gpt2'",
            "tasks": "arc_challenge",
            "num_fewshot": 25,
            "batch_size": 16,
            "data_dir": "/data1/cgzhang6/eval_datasets",
            "output_path": "./gpt2_arc_25s.json",
            "device": "cuda",
        },
    }
    evaluator = AILabEvaluator(BenchMarkType.harness, **args)
    evaluator.evaluate()
