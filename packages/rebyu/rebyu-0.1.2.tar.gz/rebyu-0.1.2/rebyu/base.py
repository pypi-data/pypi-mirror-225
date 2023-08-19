import pathlib
from typing import Any, Dict

import pandas as pd

from rebyu.pipeline.pipeline import BasePipeline


class BaseRebyu(object):
    """
    Base Class for Rebyu

    The BaseRebyu class is the foundation of Rebyu, an automatic review analysis pipeline and toolkit.
    It processes various types of data, primarily text data, using built-in pipelines designed for
    review analysis. Rebyu handles preprocessing, composition extraction, and analysis using its own
    tools and external toolsets.

    Attributes:
        data (pd.DataFrame): The input dataset, converted to a DataFrame.
        pipeline (BasePipeline): A customizable pipeline for data preprocessing, composition,
            and analysis.
        composition (Dict): Results from composition-based operations.
        analysis (Dict): Results from analysis-based operations.
        verbose (bool): Determines whether verbose output is enabled.
    """

    def __init__(self,
                 data: Any,
                 pipeline: BasePipeline,
                 verbose: bool = True):
        self.data = data
        self.pipeline = None
        self.composition = {}
        self.analysis = {}

        self.verbose = verbose

        if isinstance(data, str):
            _suffix = pathlib.Path(data).suffix

            if _suffix == '.csv':
                self.data = pd.read_csv(data)
            if _suffix == '.json':
                self.data = pd.read_json(data)

        if isinstance(data, pd.Series):
            self.data = self.data.to_frame()

        if isinstance(pipeline, BasePipeline):
            self.pipeline = pipeline

    def step(self, verbose: bool = False):
        """ Take a step of a series of process within the pipeline.

        :param verbose: Determines whether verbose output is enabled.
        :return:
        """
        if self.pipeline is None:
            return

        self.pipeline.step(
            data=self.data,
            composition=self.composition,
            analysis=self.analysis,
            verbose=verbose
        )

    def run(self, verbose: bool = False):
        """ Run through all the steps within the pipeline.

        :param verbose: Determines whether verbose output is enabled.
        :return:
        """
        if self.pipeline is None:
            return

        self.pipeline.run(
            data=self.data,
            composition=self.composition,
            analysis=self.analysis,
            verbose=verbose
        )

    def info(self):
        """ Get the information of the class.

        :return:
        """
        out_text = 'DATA:\n'
        for col in self.data.columns:
            out_text += f' -{col}: {self.data[col].dtype}\n'

        out_text += '\nCOMPOSITION:\n'
        if len(self.composition):
            for kc, vc in self.composition.items():
                out_text += f' -{kc}: {type(vc)}\n'
        else:
            out_text += 'Empty\n'

        out_text += '\nANALYSIS:\n'
        if len(self.analysis):
            for kc, vc in self.analysis.items():
                out_text += f' -{kc}: {type(vc)}\n'
        else:
            out_text += 'Empty\n'

        out_text += '\nPIPELINE:\n'
        out_text += f'pid: {self.pipeline.pid}\n'
        out_text += f'steps: {len(self.pipeline)}\n'
        out_text += f'state: {self.pipeline.state()}\n'

        out_text += '\nSTEPS:\n'
        steps_info = self.pipeline.steps_info()
        for step in steps_info:
            out_text += f' -{step}\n'

        return out_text




