import datetime
import time
from typing import Optional
from ailab.atp_evaluation.constant import Task, Model, BenchMarkType
from ailab.atp_evaluation.models import AILabModel
from ailab.atp_evaluation.benchmarks import AILabBenchmark
from ailab.atp_evaluation.benchmarks.harness import HarnessBenchmark
from ailab.log import logger

class AILabEvaluator:
    def __init__(self, benchmark_type: BenchMarkType,
                task: Task = None,
                model_name: Model = None,
                dataset_dir: str = None,
                ntrain: int = 0,
                model_dir: Optional[str] = None,
                tokenizer_dir: Optional[str] = None,
                lora_weight_dir: Optional[str] = None,
                output_dir: Optional[str] = ".",
                **args):
        if benchmark_type == BenchMarkType.harness:
            harness_args = args['harness_args']
            benchmark = HarnessBenchmark(**harness_args)
        else:
            model = AILabModel.from_pretrained('cuda', task, model_name, model_dir, lora_weight_dir, tokenizer_dir, **args)
            benchmark = AILabBenchmark.from_project_config(model, benchmark_type, dataset_dir, ntrain, output_dir, **args)
        self._benchmark = benchmark

    def evaluate(self):
        start_time = time.time()
        self._benchmark.evaluate()
        end_time = time.time()
        delta_time = datetime.timedelta(seconds=(end_time-start_time))
        logger.info(f"finished, cost time {str(delta_time)}")
