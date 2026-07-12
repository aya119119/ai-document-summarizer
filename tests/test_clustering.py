"""
Tests for src/clustering.py
"""

import os

import numpy as np
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from src.clustering import cluster_sentences, select_representative_sentences


def _make_two_topic_vectors():
    # Two obvious clusters in 2D space: around (0,0) and around (10,10)
    return np.array(
        [
            [0.0, 0.0],
            [0.1, 0.1],
            [0.2, -0.1],
            [10.0, 10.0],
            [10.1, 9.9],
            [9.9, 10.1],
        ]
    )


def test_cluster_sentences_returns_correct_number_of_clusters():
    vectors = _make_two_topic_vectors()
    model = cluster_sentences(vectors, num_clusters=2)
    assert model.n_clusters == 2
    assert len(set(model.labels_)) == 2


def test_select_representative_sentences_picks_one_per_cluster():
    vectors = _make_two_topic_vectors()
    sentences = [
        "Sentence A near origin.",
        "Sentence B near origin.",
        "Sentence C near origin.",
        "Sentence D far away.",
        "Sentence E far away.",
        "Sentence F far away.",
    ]

    result = select_representative_sentences(sentences, vectors, num_clusters=2)

    assert len(result) == 2
    # one representative should come from the "near origin" group,
    # the other from the "far away" group
    origin_group = {"Sentence A near origin.", "Sentence B near origin.", "Sentence C near origin."}
    far_group = {"Sentence D far away.", "Sentence E far away.", "Sentence F far away."}
    assert any(s in origin_group for s in result)
    assert any(s in far_group for s in result)


def test_select_representative_sentences_empty_input():
    assert select_representative_sentences([], np.array([]), num_clusters=3) == []


def test_select_representative_sentences_preserves_original_order():
    vectors = _make_two_topic_vectors()
    sentences = ["A", "B", "C", "D", "E", "F"]
    result = select_representative_sentences(sentences, vectors, num_clusters=2)
    indices = [sentences.index(s) for s in result]
    assert indices == sorted(indices)