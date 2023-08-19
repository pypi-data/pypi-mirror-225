import time

from typing import Any, Dict, List

from rebyu.base import BaseRebyu
from rebyu.pipeline.base import BasePipeline
from rebyu.pipeline import BLANK_PIPELINE


class Rebyu(BaseRebyu):
    """
    Rebyu

    The main class to access the powerful and customizable toolkit for Review Analysis.
    Rebyu takes the approach of a continuous pipeline operating under 3 categories (preprocess,
    composition, and analysis).

    Read More https://github.com/abhishtagatya/rebyu
    """

    def __init__(self,
                 data: Any,
                 pipeline: BasePipeline = BLANK_PIPELINE):
        super(Rebyu, self).__init__(data, pipeline)
