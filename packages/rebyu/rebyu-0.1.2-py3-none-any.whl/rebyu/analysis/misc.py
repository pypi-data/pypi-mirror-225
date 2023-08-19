from typing import Any, AnyStr, List

import pandas as pd
from transformers import pipeline
from transformers import AutoModel


def transformers_model(
        series: Any,
        model: Any = AutoModel,
        model_name: AnyStr = None):
    """ Predict a given series by construct a transformers model with a set of specifications

    :param series: Any series of data
    :param model: The transformers model (from transformers)
    :param model_name: The pretrained model name
    :return: List of Prediction Object
    """
    outputs = []
    _model = model.from_pretrained(model_name)

    for data in series:
        outputs.append(_model(**data))

    return outputs


def transformers_pipeline(
        series: Any,
        task: AnyStr = 'sentiment-analysis',
        model: AnyStr = None,
        **kwargs):
    """ Predict a given series by constructing a transformers pipeline with a set of specifications

    :param series: Any series of data
    :param task: The name of the task for the pretrained model
    :param model: The pretrained model name
    :param kwargs: Additional arguments to the pipeline
    :return: List of Prediction Object
    """
    pipe_task = pipeline(task=task, model=model, **kwargs)

    if isinstance(series, pd.Series):
        return pipe_task(series.tolist())

    outputs = []
    for data in series:
        outputs.append(pipe_task(data)[0])
    return outputs


