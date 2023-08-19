from typing import AnyStr, List

from rebyu.pipeline.base import BaseStep, BasePipeline


class RebyuPipeline(BasePipeline):

    """
    RebyuPipeline

    The main class to access or initiate a Rebyu Pipeline. A pipeline is a series of steps to execute.
    A pipeline can be run each step at a time, maintaining its current step to progress in the pipeline.
    """

    def __init__(self, pid: AnyStr, steps: List[BaseStep]):
        super().__init__(pid, steps)
