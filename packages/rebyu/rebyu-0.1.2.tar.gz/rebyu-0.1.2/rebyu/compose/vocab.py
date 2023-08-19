from typing import Any
from collections import Counter

from rebyu.util.dependency import nltk_dependency_mgt

from nltk.lm import Vocabulary


def counter_vocab(series: Any, cutoff: int = 2):
    """ Create a Vocabulary using the Counter class

    :param series: Any series of data
    :param cutoff: Minimum occurrence to enter the Vocab
    :return: collections.Counter
    """
    vocab = Counter()
    for data in series:
        vocab.update(data)

    for word in list(vocab):
        if vocab[word] < cutoff:
            del vocab[word]

    return vocab


def counter_character_vocab(series: Any, cutoff: int = 0):
    """ Create a Character Vocabulary using the Counter class

    :param series: Any series of data
    :param cutoff: Minimum occurrence to enter the Vocab
    :return: collections.Counter
    """
    vocab = Counter()
    for data in series:         # Per Row
        for unit in data:       # Per Token
            vocab.update(unit)  # Individual Token

    for char in list(vocab):
        if vocab[char] < cutoff:
            del vocab[char]

    return vocab


def set_character_vocab(series: Any):
    """ Create a Character Vocabulary using a Set

    :param series: Any series of data
    :return: set
    """
    vocab = set()
    for data in series:              # Per Row
        for unit in data:            # Per Token
            vocab.update(set(unit))  # Individual Token

    return vocab


def nltk_vocab(tokens: Any, cutoff: int = 2):
    """ Create a Vocabulary using NLTK Vocabulary class

    :param tokens: List of Tokens
    :param cutoff: Minimum occurrence to enter the vocab
    :return: nltk.lm.Vocabulary
    """
    nltk_dependency_mgt(required=['punkt'])

    tokenized_soup = [x for token in tokens for x in token]
    return Vocabulary(tokenized_soup, unk_cutoff=cutoff)
