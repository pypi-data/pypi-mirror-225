from typing import Any

from rebyu.util.dependency import nltk_dependency_mgt

import nltk
from nltk import pos_tag


def nltk_extract_pos_tags(series: Any):
    """ Extract Part-of-Speech Tags from a given text data using NLTK (pos_tag)

    :param series: Any series of data
    :return: Nested List of Tuples (List[List[Tuples], ...])
    """
    nltk_dependency_mgt(required=['punkt', 'averaged_perceptron_tagger'])

    pos_tags = []
    for data in series:
        if type(data) is str:
            tokens = nltk.word_tokenize(data)
        else:
            tokens = data

        pos_tags.append(pos_tag(tokens))
    return pos_tags
