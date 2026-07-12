"""
Tests for src/embeddings.py
"""

import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.embeddings import train_word_vectors, sentence_vector, build_sentence_vectors


TOKENIZED_SENTENCES = [
    ["cat", "sit", "tabl"],
    ["dog", "run", "park"],
    ["cat", "sleep", "sofa"],
]


def test_train_word_vectors_builds_vocab():
    model = train_word_vectors(TOKENIZED_SENTENCES, vector_size=20)
    assert "cat" in model.wv
    assert "dog" in model.wv
    assert model.wv["cat"].shape == (20,)


def test_sentence_vector_averages_known_tokens():
    model = train_word_vectors(TOKENIZED_SENTENCES, vector_size=20)
    vector = sentence_vector(["cat", "sit", "tabl"], model)
    assert vector.shape == (20,)
    assert not np.allclose(vector, 0)


def test_sentence_vector_unknown_tokens_returns_zero_vector():
    model = train_word_vectors(TOKENIZED_SENTENCES, vector_size=20)
    vector = sentence_vector(["unknownword"], model)
    assert np.allclose(vector, 0)


def test_build_sentence_vectors_shape():
    model = train_word_vectors(TOKENIZED_SENTENCES, vector_size=20)
    matrix = build_sentence_vectors(TOKENIZED_SENTENCES, model)
    assert matrix.shape == (3, 20)