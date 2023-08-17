from abc import ABC
import argparse
import json
import os

from ailab.atp_evaluation.build import BenchmarkRg
from ailab.atp_evaluation.constant import BenchMarkType
from ailab.log import logger
from lm_eval import tasks, evaluator, utils

@BenchmarkRg.register(BenchMarkType.harness)
class HarnessBenchmark(ABC):
    def __init__(self, **kwargs) -> None:
        default_args = self.__default_args()
        self.__model = kwargs.get("model", default_args.model)
        self.__model_args = kwargs.get("model_args", default_args.model_args)
        self.__tasks = kwargs.get("tasks", default_args.tasks)
        self.__provide_description = kwargs.get("provide_description", default_args.provide_description)
        self.__num_fewshot = kwargs.get("num_fewshot", default_args.num_fewshot)
        self.__batch_size = kwargs.get("batch_size", default_args.batch_size)
        self.__max_batch_size = kwargs.get("max_batch_size", default_args.max_batch_size)
        self.__device = kwargs.get("device", default_args.device)
        self.__output_path = kwargs.get("output_path", default_args.output_path)
        self.__limit = kwargs.get("limit", default_args.limit)
        self.__data_sampling = kwargs.get("data_sampling", default_args.data_sampling)
        self.__no_cache = kwargs.get("no_cache", default_args.no_cache)
        self.__decontamination_ngrams_path = kwargs.get("decontamination_ngrams_path", default_args.decontamination_ngrams_path)
        self.__description_dict_path = kwargs.get("description_dict_path", default_args.description_dict_path)
        self.__check_integrity = kwargs.get("check_integrity", default_args.check_integrity)
        self.__write_out = kwargs.get("write_out", default_args.write_out)
        self.__output_base_path = kwargs.get("output_base_path", default_args.output_base_path)
        self.__data_dir = kwargs.get("data_dir", default_args.data_dir)

        assert not self.__provide_description  # not implemented

        if self.__limit:
            logger.info(
                "WARNING: --limit SHOULD ONLY BE USED FOR TESTING. REAL METRICS SHOULD NOT BE COMPUTED USING LIMIT."
            )

        if self.__tasks is None:
            self.__task_names = tasks.ALL_TASKS
        else:
            self.__task_names = utils.pattern_match(self.__tasks.split(","), tasks.ALL_TASKS)

        logger.info(f"Selected Tasks: {self.__task_names}")

        self.__description_dict = {}
        if self.__description_dict_path:
            with open(self.__description_dict_path, "r") as f:
                self.__description_dict = json.load(f)

    def evaluate(self):
        results = evaluator.simple_evaluate(
            model=self.__model,
            model_args=self.__model_args,
            tasks=self.__task_names,
            num_fewshot=self.__num_fewshot,
            batch_size=self.__batch_size,
            max_batch_size=self.__max_batch_size,
            device=self.__device,
            no_cache=self.__no_cache,
            limit=self.__limit,
            description_dict=self.__description_dict,
            decontamination_ngrams_path=self.__decontamination_ngrams_path,
            check_integrity=self.__check_integrity,
            write_out=self.__write_out,
            output_base_path=self.__output_base_path,
            data_dir=self.__data_dir,
        )

        dumped = json.dumps(results, indent=2)
        logger.info(dumped)

        if self.__output_path:
            os.makedirs(os.path.dirname(self.__output_path), exist_ok=True)
            with open(self.__output_path, "w") as f:
                f.write(dumped)

        batch_sizes = ",".join(map(str, results["config"]["batch_sizes"]))
        logger.info(
            f"{self.__model} ({self.__model_args}), limit: {self.__limit}, provide_description: {self.__provide_description}, "
            f"num_fewshot: {self.__num_fewshot}, batch_size: {self.__batch_size}{f' ({batch_sizes})' if batch_sizes else ''}"
        )
        print(evaluator.make_table(results))

    def __default_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--model", default=None)
        parser.add_argument("--model_args", default="")
        parser.add_argument("--tasks", default=None, choices=utils.MultiChoice(tasks.ALL_TASKS))
        parser.add_argument("--provide_description", action="store_true")
        parser.add_argument("--num_fewshot", type=int, default=0)
        parser.add_argument("--batch_size", type=str, default=None)
        parser.add_argument("--max_batch_size", type=int, default=None,
                            help="Maximal batch size to try with --batch_size auto")
        parser.add_argument("--device", type=str, default=None)
        parser.add_argument("--output_path", default=None)
        parser.add_argument("--limit", type=float, default=None,
                            help="Limit the number of examples per task. "
                                "If <1, limit is a percentage of the total number of examples.")
        parser.add_argument("--data_sampling", type=float, default=None)
        parser.add_argument("--no_cache", action="store_true")
        parser.add_argument("--decontamination_ngrams_path", default=None)
        parser.add_argument("--description_dict_path", default=None)
        parser.add_argument("--check_integrity", action="store_true")
        parser.add_argument("--write_out", action="store_true", default=False)
        parser.add_argument("--output_base_path", type=str, default=None)
        parser.add_argument("--data_dir", type=str, default=None)

        return parser.parse_args([])
