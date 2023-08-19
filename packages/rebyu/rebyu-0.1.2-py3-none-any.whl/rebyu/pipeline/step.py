from typing import Any, AnyStr, Dict

from rebyu.pipeline.base import BaseStep
from rebyu.preprocess.remove import (
    remove_numbers,
    remove_punctuations,
    remove_whitespaces,
    remove_specifics,
    remove_urls,
    remove_stopwords
)
from rebyu.preprocess.transform import (
    cast_nan_str,
    cast_case,
    sub_replace,
    expand_contractions,
    censor_username,
    censor_urls,

    # TextBlob
    to_textblob,
    textblob_tokenize,
    textblob_sentences,

    # NLTK
    nltk_tokenize,
    nltk_porter_stem,
    nltk_lancaster_stem,
    nltk_wordnet_lemma,

    # Transformers
    transformers_tokenize
)
from rebyu.compose.vocab import (
    counter_vocab,
    counter_character_vocab,
    set_character_vocab,

    # NLTK
    nltk_vocab
)
from rebyu.compose.ner import nltk_extract_ner
from rebyu.compose.pos import nltk_extract_pos_tags
from rebyu.analysis.sentiment import (
    # TextBlob
    textblob_polarity,

    # NLTK
    vader_polarity
)
from rebyu.analysis.misc import (
    transformers_model,
    transformers_pipeline
)


class RebyuStep(BaseStep):
    """
    RebyuStep

    The main class to access or initiate a Rebyu Step. A step is an encapsulated function to operate under a
    pipeline which Rebyu provides. The function takes a source of data (which would be a key from the Rebyu.data)
    DataFrame and a target to output its data. The behaviour of the operation may differ depending on the
    type of step it is. It can be PREPROCESS, COMPOSE, or ANALYZE.
    """

    def __init__(self,
                 sid: AnyStr,
                 stype: AnyStr,
                 source: Any,
                 target: Any,
                 func: Any,
                 func_args: Dict[AnyStr, Any] = None):
        super(RebyuStep, self).__init__(
            sid=sid,
            stype=stype,
            source=source,
            target=target,
            func=func,
            func_args=func_args
        )


PREP_CAST_NAN = RebyuStep(
    sid='rb-cast_nan',
    stype=RebyuStep.STEP_PREPROCESS,
    source='text',
    target='text',
    func=cast_nan_str
)
"""Convert non-string data in 'text' (Rebyu.data) to an empty string."""

PREP_CAST_CASE = RebyuStep(
    sid='rb-cast_case',
    stype=RebyuStep.STEP_PREPROCESS,
    source='text',
    target='text',
    func=cast_case
)
"""Switch case the data in 'text' (Rebyu.data) to lower or upper case."""

PREP_REMOVE_NUMBERS = RebyuStep(
    sid='rb-remove_numbers',
    stype=RebyuStep.STEP_PREPROCESS,
    source='text',
    target='text',
    func=remove_numbers
)
"""Remove numerical data in 'text' (Rebyu.data)"""

PREP_REMOVE_PUNCTUATIONS = RebyuStep(
    sid='rb-remove_punctuations',
    stype=RebyuStep.STEP_PREPROCESS,
    source='text',
    target='text',
    func=remove_punctuations
)
"""Remove punctuations in 'text' (Rebyu.data)"""

PREP_REMOVE_WHITESPACES = RebyuStep(
    sid='rb-remove_whitespaces',
    stype=RebyuStep.STEP_PREPROCESS,
    source='text',
    target='text',
    func=remove_whitespaces
)
"""Remove whitespaces in 'text' (Rebyu.data)"""

PREP_REMOVE_SPECIFICS = RebyuStep(
    sid='rb-remove_specifics',
    stype=RebyuStep.STEP_PREPROCESS,
    source='text',
    target='text',
    func=remove_specifics
)
"""Remove specific substring in 'text' (Rebyu.data)"""

PREP_REMOVE_URLS = RebyuStep(
    sid='rb-remove_urls',
    stype=RebyuStep.STEP_PREPROCESS,
    source='text',
    target='text',
    func=remove_urls
)
"""Remove urls in 'text' (Rebyu.data)"""

PREP_REMOVE_STOPWORDS = RebyuStep(
    sid='rb-remove_stopwords',
    stype=RebyuStep.STEP_PREPROCESS,
    source='text',
    target='text',
    func=remove_stopwords
)
"""Remove stopwords in 'text' (Rebyu.data)"""

PREP_REPLACE_WORD = RebyuStep(
    sid='rb-sub_replace',
    stype=BaseStep.STEP_PREPROCESS,
    source='text',
    target='text',
    func=sub_replace
)
"""Replace substring in 'text' (Rebyu.data)"""

PREP_EXPAND_CONTRACTIONS = RebyuStep(
    sid='rb-expand_contractions',
    stype=BaseStep.STEP_PREPROCESS,
    source='text',
    target='text',
    func=expand_contractions
)
"""Replace contractions in 'text' (Rebyu.data) to full words"""

PREP_CENSOR_USERNAME = RebyuStep(
    sid='rb-censor_username',
    stype=BaseStep.STEP_PREPROCESS,
    source='text',
    target='text',
    func=censor_username
)
"""Censor any username in 'text' (Rebyu.data) to a placeholder"""

PREP_CENSOR_URLS = RebyuStep(
    sid='rb-censor_urls',
    stype=BaseStep.STEP_PREPROCESS,
    source='text',
    target='text',
    func=censor_urls
)
"""Censor any urls in 'text' (Rebyu.data) to a placeholder"""

PREP_SENTENCE_LENGTH = RebyuStep(
    sid='rb-sentence_length',
    stype=BaseStep.STEP_PREPROCESS,
    source='text',
    target='length',
    func=lambda x: len(x) if type(x) is str else ''
)
"""Return the sentence length of 'text' (Rebyu.data) to 'length'"""

PREP_WORD_COUNT = RebyuStep(
    sid='rb-word_count',
    stype=BaseStep.STEP_PREPROCESS,
    source='tokens',
    target='word_counts',
    func=lambda x: len(x)
)
"""Return the word count of 'text' (Rebyu.data) to 'word_counts'"""

COMPOSE_COUNTER_VOCAB = RebyuStep(
    sid='rb-counter_vocab',
    stype=BaseStep.STEP_COMPOSE,
    source='tokens',
    target='vocab',
    func=counter_vocab
)
"""Compose a vocabulary from 'tokens' (Rebyu.data) to 'vocab' using Counter from collections"""

COMPOSE_COUNTER_CHARVOCAB = RebyuStep(
    sid='rb-counter_charvocab',
    stype=BaseStep.STEP_COMPOSE,
    source='tokens',
    target='char_vocab',
    func=counter_character_vocab
)
"""Compose a character set from 'tokens' (Rebyu.data) to 'char_vocab' using Counter from collections"""

COMPOSE_SET_CHARVOCAB = RebyuStep(
    sid='rb-set_charvocab',
    stype=BaseStep.STEP_COMPOSE,
    source='tokens',
    target='char_vocab',
    func=set_character_vocab
)
"""Compose a character set from 'tokens' (Rebyu.data) to 'char_vocab' using a built-in set"""


# -- TextBlob -- #

PREP_TEXTBLOB = RebyuStep(
    sid='rb-to_textblob',
    stype=BaseStep.STEP_PREPROCESS,
    source='text',
    target='text',
    func=to_textblob
)
"""Converts data into a TextBlob object from 'text' (Rebyu.data)"""

PREP_TEXTBLOB_TOKENIZE = RebyuStep(
    sid='rb-textblob_tokenize',
    stype=BaseStep.STEP_PREPROCESS,
    source='text',
    target='tokens',
    func=textblob_tokenize
)
"""Tokenize 'text' (Rebyu.data) into 'tokens' using `TextBlob.tokens`"""

PREP_TEXTBLOB_SENTENCES = RebyuStep(
    sid='rb-textblob_sentences',
    stype=BaseStep.STEP_PREPROCESS,
    source='text',
    target='sentences',
    func=textblob_sentences
)
"""Extract sentences from 'text' (Rebyu.data) into 'sentences' using `TextBlob.sentences`"""

ANALYZE_TEXTBLOB_POLARITY = RebyuStep(
    sid='rb-textblob_polarity',
    stype=BaseStep.STEP_ANALYZE,
    source='text',
    target='textblob_polarity',
    func=textblob_polarity
)
"""Predict the polarity of 'text' (Rebyu.data) into 'textblob_polarity' using `TextBlob.polarity`"""

# -- NLTK -- #

PREP_NLTK_TOKENIZE = RebyuStep(
    sid='rb-tokenize',
    stype=BaseStep.STEP_PREPROCESS,
    source='text',
    target='tokens',
    func=nltk_tokenize
)
"""Tokenize 'text' (Rebyu.data) into 'tokens' using `nltk.word_tokenize`"""

PREP_NLTK_PORTER_STEM = RebyuStep(
    sid='rb-porter_stem',
    stype=BaseStep.STEP_PREPROCESS,
    source='text',
    target='text',
    func=nltk_porter_stem
)
"""Stem each word from 'text' (Rebyu.data) using the Porter method from NLTK"""

PREP_NLTK_LANCASTER_STEM = RebyuStep(
    sid='rb-porter_stem',
    stype=BaseStep.STEP_PREPROCESS,
    source='text',
    target='text',
    func=nltk_lancaster_stem
)
"""Stem each word from 'text' (Rebyu.data) using the Lancaster method from NLTK"""

PREP_NLTK_WORDNET_LEMMA = RebyuStep(
    sid='rb-wordnet_lemma',
    stype=BaseStep.STEP_PREPROCESS,
    source='text',
    target='text',
    func=nltk_wordnet_lemma
)
"""Lemmatize each word from 'text' (Rebyu.data) using WordNET from NLTK"""

COMPOSE_NLTK_VOCAB = RebyuStep(
    sid='rb-nltk_vocab',
    stype=BaseStep.STEP_COMPOSE,
    source='tokens',
    target='vocab',
    func=nltk_vocab
)
"""Compose a vocabulary 'tokens' (Rebyu.data) using NLTK's Vocabulary class"""

COMPOSE_NLTK_POS_TAG = RebyuStep(
    sid='rb-nltk_pos_tag',
    stype=BaseStep.STEP_COMPOSE,
    source='tokens',
    target='pos_tags',
    func=nltk_extract_pos_tags
)
"""Extract Part-of-Speech Tags from 'tokens' (Rebyu.data) using NLTK's pos_tag"""

COMPOSE_NLTK_NER = RebyuStep(
    sid='rb-nltk_ner',
    stype=BaseStep.STEP_COMPOSE,
    source='tokens',
    target='ner',
    func=nltk_extract_ner
)
"""Extract Named Entities from 'tokens' (Rebyu.data) using NLTK's ne_chunk"""

ANALYZE_VADER_POLARITY = RebyuStep(
    sid='rb-vader_polarity',
    stype=BaseStep.STEP_ANALYZE,
    source='text',
    target='vader_polarity',
    func=vader_polarity
)
"""Predict the polarity of 'text' (Rebyu.data) into 'vader_polarity' using the VADER algorithm"""

# -- Transformers -- #

PREP_TRANSFORMERS_TOKENIZE = RebyuStep(
    sid='rb-transformers_tokenize',
    stype=BaseStep.STEP_PREPROCESS,
    source='text',
    target='tokens',
    func=transformers_tokenize
)
"""Tokenize 'text' (Rebyu.data) into 'tokens' using transformers module tokenizers

See the `transformers_tokenize` documentation."""

ANALYZE_TRANSFORMERS_MODEL = RebyuStep(
    sid='rb-transformers_model',
    stype=BaseStep.STEP_ANALYZE,
    source='tokens',
    target='transformers_analysis',
    func=transformers_model
)
"""Predict values from 'tokens' (Rebyu.data) into an analysis in 'transformers_analysis'. It uses models from the 
transformers module. 

See the `transformers_model` documentation."""

ANALYZE_TRANSFORMERS_PIPELINE = RebyuStep(
    sid='rb-transformers_pipeline',
    stype=BaseStep.STEP_ANALYZE,
    source='text',
    target='transformers_analysis',
    func=transformers_pipeline
)
"""Construct a pipeline from the transformers module. Taking 'text' (Rebyu.data) into an analysis in 
'transformers_analysis' 

See the `transformers_pipeline` documentation."""

ANALYZE_CARDIFFNLP_SENTIMENT = RebyuStep(
    sid='cardiffnlp_sentiment',
    stype=BaseStep.STEP_ANALYZE,
    source='text',
    target='sentiment',
    func=transformers_pipeline,
    func_args={
        'task': 'sentiment-analysis',
        'model': 'cardiffnlp/twitter-roberta-base-sentiment-latest'
    }
)
"""Construct a pipeline from the transformers module specific for Cardiff NLP Sentiment Analysis Tasks.
Taking 'text' (Rebyu.data) into an analysis in 'sentiment' 

See the `transformers_pipeline` documentation."""

ANALYZE_CARDIFFNLP_EMOTION = RebyuStep(
    sid='cardiffnlp_emotion',
    stype=BaseStep.STEP_ANALYZE,
    source='text',
    target='emotion',
    func=transformers_pipeline,
    func_args={
        'task': 'text-classification',
        'model': 'cardiffnlp/twitter-roberta-base-emotion-multilabel-latest',
        'top_k': 10
    }
)
"""Construct a pipeline from the transformers module specific for Cardiff NLP Emotion Analysis Tasks.
Taking 'text' (Rebyu.data) into an analysis in 'emotion' 

See the `transformers_pipeline` documentation."""

ANALYZE_FINITEAUTOMATA_SENTIMENT = RebyuStep(
    sid='finiteautomata_sentiment',
    stype=BaseStep.STEP_ANALYZE,
    source='text',
    target='sentiment',
    func=transformers_pipeline,
    func_args={
        'task': 'text-classification',
        'model': 'finiteautomata/bertweet-base-sentiment-analysis'
    }
)
"""Construct a pipeline from the transformers module specific for @finiteautomata Sentiment Analysis Tasks.
Taking 'text' (Rebyu.data) into an analysis in 'sentiment' 

See the `transformers_pipeline` documentation."""

ANALYZE_FINITEAUTOMATA_EMOTION = RebyuStep(
    sid='finiteautomata_emotion',
    stype=BaseStep.STEP_ANALYZE,
    source='text',
    target='emotion',
    func=transformers_pipeline,
    func_args={
        'task': 'text-classification',
        'model': 'finiteautomata/bertweet-base-emotion-analysis',
        'top_k': 5
    }
)
"""Construct a pipeline from the transformers module specific for @finiteautomata Emotion Analysis Tasks.
Taking 'text' (Rebyu.data) into an analysis in 'emotion' 

See the `transformers_pipeline` documentation."""