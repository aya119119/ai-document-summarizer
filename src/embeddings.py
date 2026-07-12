"""
embeddings.py

Turns tokenized sentences into numerical vectors using word embeddings.

A lightweight Word2Vec model is trained directly on the document's own
tokens (no large pretrained file to download), then each sentence is
represented as the average of its word vectors.
"""

import numpy as np
from gensim.models import Word2Vec


DEFAULT_VECTOR_SIZE = 100


def train_word_vectors(
    tokenized_sentences: list[list[str]],
    vector_size: int = DEFAULT_VECTOR_SIZE,
    window: int = 5,
    min_count: int = 1,
) -> Word2Vec:
    """
    Train a Word2Vec model on the document's tokenized sentences.

    Args:
        tokenized_sentences: Output of nlp_pipeline.process_text, i.e. a
            list of sentences, each a list of normalized tokens.
        vector_size: Dimensionality of the word vectors.
        window: Context window size used during training.
        min_count: Minimum token frequency to be included in the vocabulary.

    Returns:
        A trained gensim Word2Vec model.
    """
    return Word2Vec(
        sentences=tokenized_sentences,
        vector_size=vector_size,
        window=window,
        min_count=min_count,
        workers=1,
        seed=42,
    )


def sentence_vector(tokens: list[str], model: Word2Vec) -> np.ndarray:
    """
    Represent a single tokenized sentence as the average of its word vectors.

    Tokens not present in the model's vocabulary are skipped. If none of
    the tokens are known, a zero vector is returned.

    Args:
        tokens: Normalized tokens for one sentence.
        model: A trained Word2Vec model.

    Returns:
        A vector of shape (vector_size,).
    """
    vectors = [model.wv[token] for token in tokens if token in model.wv]

    if not vectors:
        return np.zeros(model.vector_size)

    return np.mean(vectors, axis=0)


def build_sentence_vectors(
    tokenized_sentences: list[list[str]], model: Word2Vec
) -> np.ndarray:
    """
    Build a matrix of sentence vectors for an entire document.

    Args:
        tokenized_sentences: A list of sentences, each a list of tokens.
        model: A trained Word2Vec model.

    Returns:
        A matrix of shape (num_sentences, vector_size).
    """
    return np.array(
        [sentence_vector(tokens, model) for tokens in tokenized_sentences]
    )