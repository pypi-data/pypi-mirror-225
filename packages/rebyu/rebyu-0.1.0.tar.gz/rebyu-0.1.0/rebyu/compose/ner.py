from typing import Any

from rebyu.util.dependency import nltk_dependency_mgt

import nltk
from nltk import pos_tag
from nltk.chunk import ne_chunk


def nltk_extract_ner(series: Any):
    """ Extract Named-Entities from a given text data using NLTK (ne_chunk)

    :param series: Any series of data
    :return: Nested List of Tuples (List[List[Tuples], ...])
    """
    nltk_dependency_mgt(required=[
        'punkt', 'maxent_ne_chunker', 'words', 'averaged_perceptron_tagger'
    ])

    entities = []
    for data in series:
        if type(data) is str:
            tokens = nltk.word_tokenize(data)
        else:
            tokens = data

        tags = pos_tag(tokens)
        ner_chunks = ne_chunk(tags)

        named_entities = []
        for subtree in ner_chunks:
            if type(subtree) == nltk.Tree:
                entity = ' '.join([word for word, tag in subtree.leaves()])
                entity_type = subtree.label()
                named_entities.append((entity, entity_type))
        entities.append(named_entities)
    return entities
