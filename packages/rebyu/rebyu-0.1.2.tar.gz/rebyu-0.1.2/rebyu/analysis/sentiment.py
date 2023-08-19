from typing import Any

from rebyu.util.dependency import nltk_dependency_mgt

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob


def textblob_polarity(series: Any):
    """ Predict the polarity of a given text data using TextBlob

    :param series: Any series of data
    :return: List of Dict (TextBlob Polarity)
    """
    nltk_dependency_mgt(required=['vader_lexicon'])

    polarities = []
    for text in series:
        if isinstance(text, TextBlob):
            polarities.append(text.polarity)
        else:
            polarities.append(TextBlob(text).polarity)
    return polarities


def vader_polarity(series: Any):
    """ Predict the polarity of a given text data using VADER

    :param series: Any series of data
    :return: List of Dict (Vader Polarity)
    """
    polarities = []
    analyzer = SentimentIntensityAnalyzer()
    for text in series:
        if isinstance(text, TextBlob):
            polarities.append(analyzer.polarity_scores(text.raw))
        else:
            polarities.append(analyzer.polarity_scores(text))
    return polarities

