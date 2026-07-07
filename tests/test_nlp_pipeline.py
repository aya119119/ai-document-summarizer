"""
Tests for src/nlp_pipeline.py
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.nlp_pipeline import split_sentences, process_sentence, process_text


def test_split_sentences():
    text = "This is one sentence. This is another one."
    sentences = split_sentences(text)
    assert sentences == ["This is one sentence.", "This is another one."]


def test_split_sentences_empty():
    assert split_sentences("") == []


def test_process_sentence_removes_stopwords_and_punctuation():
    sentence = "The cat is sitting on the table."
    tokens = process_sentence(sentence)
    assert "the" not in tokens
    assert "is" not in tokens
    assert "." not in tokens


def test_process_sentence_stems_words():
    sentence = "running runs ran"
    tokens = process_sentence(sentence)
    assert all(token == "run" for token in tokens)


def test_process_text_returns_list_per_sentence():
    text = "First sentence here. Second sentence here."
    result = process_text(text)
    assert len(result) == 2
    assert isinstance(result[0], list)