import re
import string
from typing import List, Any, AnyStr

import nltk
from nltk.corpus import stopwords

from rebyu.util.dependency import nltk_dependency_mgt

NUMBERS_REGEX = r'\d+'
URLS_REGEX = r'(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z]{2,}(\.[a-zA-Z]{2,})(\.[a-zA-Z]{2,' \
             r'})?\/[a-zA-Z0-9]{2,}|((https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z]{2,}(\.[a-zA-Z]{2,' \
             r'})(\.[a-zA-Z]{2,})?)|(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z0-9]{2,' \
             r'}\.[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,}(\.[a-zA-Z0-9]{2,})? '


def remove_patterns(text: Any, pattern: AnyStr):
    """ Remove patterns (regex) from a text

    :param text: Any string object
    :param pattern: Any string object
    :return: text
    """
    if type(text) is str:
        return re.sub(pattern, '', text)
    return text


def remove_numbers(text: Any, pattern: AnyStr = NUMBERS_REGEX):
    """ Remove numerical data from text (using a regex pattern)

    :param text: Any string object
    :param pattern: Any string object
    :return: text
    """
    return remove_patterns(text, pattern)


def remove_urls(text: Any, pattern: AnyStr = URLS_REGEX):
    """ Remove urls from text (using a regex pattern)

    :param text: Any string object
    :param pattern: Any string object
    :return: text
    """
    return remove_patterns(text, pattern)


def remove_punctuations(text: Any):
    """ Remove punctuations from text (from string.punctuation)

    :param text: Any string object
    :return: text
    """
    if type(text) is str:
        return text.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))
    return text


def remove_whitespaces(text: Any):
    """ Strip any whitespaces from text

    :param text: Any string object
    :return: text
    """
    if type(text) is str:
        return text.strip()
    return text


def remove_specifics(text: Any, sub: Any):
    """ Remove specific substring from text

    :param text: Any string object
    :param sub: Any string object
    :return: text
    """
    if type(text) is str and type(sub) is str:
        return text.replace(sub, '')
    return text


# -- NLTK -- #

def remove_stopwords(text: Any, extra: List[Any] = None, language: str = 'english'):
    """ Remove stopwords from text (using NLTK Stopwords)

    :param text: Any string object
    :param extra: List of Any string objects
    :param language: The language of the text
    :return: text
    """

    nltk_dependency_mgt(required=['punkt', 'stopwords'])

    stop_words = set(stopwords.words(language) + (extra or []))
    tokens = nltk.word_tokenize(text)
    filtered_tokens = filter(lambda x: x.lower() not in stop_words, tokens)

    if type(text) is str:
        return ' '.join(filtered_tokens)
    return filtered_tokens
