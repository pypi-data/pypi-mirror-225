import copy

import pandas as pd

from typing import Any, AnyStr, List, Dict, Optional

from rebyu.util.logger import Logger


class BaseStep(object):
    """
    Base Class for Step

    The BaseStep class is the foundation of Rebyu Steps which are encapsulated functions to run
    within a pipeline with a given rule-set. Primarily, the step takes 3 run-types, which are preprocessor,
    composer, and analyzer.
    """
    STEP_PREPROCESS = "PREPROCESS"
    STEP_COMPOSE = "COMPOSE"
    STEP_ANALYZE = "ANALYZE"

    def __init__(self,
                 sid: AnyStr,
                 stype: AnyStr,
                 source: Any,
                 target: Any,
                 func: Any,
                 func_args: Dict[AnyStr, Any] = None):
        self.sid = sid
        self.stype = stype
        self.source = source
        self.target = target
        self.func = func
        self.func_args = func_args or {}

        self.next = None

    def run(self, data: pd.DataFrame, composition: Dict, analysis: Dict):
        """ Run the step according to it's type.

        - PREPROCESS: Takes data from Rebyu.data as source to operate and output to the target column.
        - COMPOSE: Takes data from Rebyu.data as source to operate and output to a composition dict store with target as key.
        - ANALYZE: Takes data from Rebyu.data as source to operate and output to a analysis dict store with target as key.

        :param data: The input dataset (pd.DataFrame).
        :param composition: The composition store (Dict).
        :param analysis: The analysis store (Dict).
        :return: data, composition, analysis.
        """
        if self.stype == self.STEP_PREPROCESS:
            data[self.target] = data[self.source].apply(self.func, **self.func_args)

        if self.stype == self.STEP_COMPOSE:
            composition[self.target] = self.func(data[self.source], **self.func_args)

        if self.stype == self.STEP_ANALYZE:
            analysis[self.target] = self.func(data[self.source], **self.func_args)

        return data, composition, analysis

    def copy(self, deep: bool = True):
        """ Copy the instance of this class.

        :param deep: Determines whether it will be a deepcopy.
        :return: BaseStep.
        """
        if deep:
            return copy.deepcopy(self)
        return copy.copy(self)

    def add_args(self, **kwargs):
        """ Add function arguments to BaseStep.func function.

        :param kwargs:
        :return: BaseStep.
        """
        self.func_args.update({k: v for k, v in kwargs.items()})
        return self

    def set_sid(self, sid: AnyStr):
        """ Change Step ID.

        :param sid: Step ID.
        :return: BaseStep.
        """
        self.sid = sid
        return self

    def set_stype(self, stype: AnyStr):
        """ Change Step Type.

        :param stype: Step Type (BaseStep.STEP_PREPROCESS, BaseStep.STEP_COMPOSE, BaseStep.STEP_ANALYZE).
        :return: BaseStep.
        """
        self.stype = stype
        return self

    def set_source(self, source: AnyStr):
        """ Change Source of Data (Column from Rebyu.data).

        :param source: Source Key (Rebyu.data) Key.
        :return: BaseStep.
        """
        self.source = source
        return self

    def set_target(self, target: AnyStr):
        """ Change Target of Data (Column from Rebyu.data).

        :param target: Target Key (Rebyu.data, Rebyu.composition, Rebyu.analysis) Key.
        :return: BaseStep.
        """
        self.target = target
        return self

    def set_func(self, func: Any):
        """ Change Function.

        :param func: Function Object.
        :return:
        """
        self.func = func
        return self

    def __repr__(self):
        return f'Step(sid={self.sid}, stype={self.stype}, source={self.source}, target={self.target})'


class BasePipeline(object):

    def __init__(self, pid: AnyStr, steps: List[BaseStep]):
        self.pid = pid
        self.head: Optional[BaseStep] = None
        self.tail: Optional[BaseStep] = None
        self.curr_idx, self.curr = (0, self.head)
        self.length = 0

        self.pipeline_logger = Logger(self.__class__.__name__)
        self._prepare_pipeline(steps)

    def _prepare_pipeline(self, steps: List[BaseStep]):
        """ Prepare Pipeline Steps into Linked List

        :param steps: List of Steps.
        :return:
        """
        for step in steps:
            self.add(step)

    def step(self,
             data: pd.DataFrame,
             composition: Dict,
             analysis: Dict,
             verbose: bool = False) -> bool:
        """ Take a step into the pipeline. Processing the next step to operate.

        :param data: The input dataset (pd.DataFrame).
        :param composition: The composition store (Dict).
        :param analysis: The analysis store (Dict).
        :param verbose: Determines whether verbose output is enabled.
        :return:
        """
        if self.head is None:
            return False

        if self.curr is None:
            return False

        if verbose:
            self.pipeline_logger.info(f'[{self.curr.stype}] - Running step {self.curr.sid}')

        self.curr.run(data=data, composition=composition, analysis=analysis)

        if verbose:
            self.pipeline_logger.info(f'[{self.curr.stype}] - Finished step {self.curr.sid}')

        self.curr = self.curr.next
        self.curr_idx += 1

        return True

    def run(self, data: pd.DataFrame, composition: Dict, analysis: Dict, verbose: bool = False):
        """ Run through the steps in the pipeline. Processing all the steps to operate.

        :param data: The input dataset (pd.DataFrame).
        :param composition: The composition store (Dict).
        :param analysis: The analysis store (Dict).
        :param verbose: Determines whether verbose output is enabled.
        :return:
        """
        self.pipeline_logger.info(f'[{self.pid}] - Running pipeline')
        out = True
        while out:
            out = self.step(
                data=data,
                composition=composition,
                analysis=analysis,
                verbose=verbose
            )
        self.pipeline_logger.info(f'[{self.pid}] - Finished pipeline')

    def add(self, step: BaseStep) -> BaseStep:
        """ Add a new step to the pipeline.

        :param step: BaseStep
        :return: BaseStep
        """
        new_step = step.copy()
        return self._add_node(new_step)

    def add_function(self,
                     func: object,
                     stype: AnyStr,
                     source: AnyStr,
                     target: AnyStr,
                     func_args: Dict = None) -> BaseStep:
        """ Add a new step to the pipeline via functions

        :param func: Function
        :param stype: Step Type (BaseStep.STEP_PREPROCESS, BaseStep.STEP_COMPOSE, BaseStep.STEP_ANALYZE).
        :param source: Source Key (Rebyu.data) Key.
        :param target: Target Key (Rebyu.data, Rebyu.composition, Rebyu.analysis) Key.
        :param func_args: Function arguments (Dict)
        :return: BaseStep
        """
        new_step = BaseStep(
            sid=func.__name__,
            stype=stype,
            source=source,
            target=target,
            func=func,
            func_args=func_args
        )

        return self._add_node(new_step)

    def _add_node(self, new_step: BaseStep) -> BaseStep:
        if self.head is None:
            self.head = new_step
            self.tail = new_step
            self.curr_idx, self.curr = (0, self.head)
        else:
            self.tail.next = new_step
            self.tail = new_step

        self.length += 1
        return new_step

    def pop(self) -> Optional[BaseStep]:
        """ Remove last step in the pipeline.

        :return: BaseStep | None
        """
        if self.head is None:
            return None

        if self.head == self.tail:
            step = self.head
            self.head = None
            self.tail = None
            self.length -= 1
            return step

        current = self.head
        while current.next != self.tail:
            current = current.next

        step = self.tail
        current.next = None
        self.tail = current
        self.length -= 1
        return step

    def steps_info(self) -> List[BaseStep]:
        """ Get the information of all the steps in the pipeline.

        :return: List of BaseSteps
        """
        out = []
        current = self.head
        while current:
            out.append(current)
            current = current.next
        return out

    def state(self) -> (Optional[int], Optional[BaseStep]):
        """ Get the current state of the pipeline progress.

        :return: State of Index and Current Step
        """
        return self.curr_idx, self.curr

    def reset(self):
        """ Reset the current state (Index and Step) of the pipeline.

        :return:
        """
        self.curr = self.head
        self.curr_idx = 0
        return

    def __len__(self):
        return self.length

    def __repr__(self):
        return f'Pipeline(pid={self.pid})'
