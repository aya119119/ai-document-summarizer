"""
Tests for src/summarizer.py
"""

from src.summarizer import summarize_text, get_document_stats


LONG_TEXT = """
Artificial intelligence is transforming healthcare in profound ways.
Doctors now use machine learning models to detect diseases earlier than ever before.
Hospitals are adopting AI-powered tools to manage patient records efficiently.
Researchers are using AI to accelerate the discovery of new drugs.
Patients benefit from more accurate diagnoses thanks to these technologies.
However, concerns remain about data privacy and algorithmic bias in medical AI.
Despite these challenges, the overall impact of AI on healthcare continues to grow.
"""


def test_summarize_text_returns_fewer_sentences_than_original():
    summary = summarize_text(LONG_TEXT, num_sentences=3)
    original_sentence_count = len(
        [s for s in LONG_TEXT.strip().split(".") if s.strip()]
    )
    summary_sentence_count = len([s for s in summary.split(".") if s.strip()])
    assert summary_sentence_count <= 3
    assert summary_sentence_count < original_sentence_count


def test_summarize_text_short_input_returns_everything():
    short_text = "This is one sentence. This is another."
    summary = summarize_text(short_text, num_sentences=5)
    assert "This is one sentence." in summary
    assert "This is another." in summary


def test_summarize_text_empty_input():
    assert summarize_text("", num_sentences=3) == ""


def test_get_document_stats_reports_compression():
    summary = summarize_text(LONG_TEXT, num_sentences=3)
    stats = get_document_stats(LONG_TEXT, summary)

    assert stats["original_word_count"] > 0
    assert stats["summary_word_count"] > 0
    assert stats["summary_word_count"] <= stats["original_word_count"]
    assert 0 <= stats["compression_ratio"] <= 1