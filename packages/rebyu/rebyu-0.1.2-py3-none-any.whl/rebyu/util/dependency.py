from typing import List

import nltk


def nltk_dependency_mgt(required: List[str] = None):
    """ Check and Fulfill required dependencies for NLTK

    :param required: List of String (packages)
    :return:
    """
    nltk_lookup = {
        'punkt': 'tokenizers/punkt',
        'stopwords': 'corpora/stopwords',
        'wordnet': 'corpora/wordnet',
        'words': 'corpora/words',
        'averaged_perceptron_tagger': 'taggers/averaged_perceptron_tagger',
        'vader_lexicon': 'sentiment/vader_lexicon',
        'maxent_ne_chunker': 'chunkers/maxent_ne_chunker'
    }

    if required is None:
        return

    for resource in required:
        try:
            nltk.data.find(nltk_lookup.get(resource, f'corpora/{resource}'))
        except LookupError:
            nltk.download(resource)
    return
