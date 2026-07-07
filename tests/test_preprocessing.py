"""
Tests for src/preprocessing.py
command used : python -m pytest tests\test_preprocessing.py -v
"""

from src.preprocessing import clean_text


def test_clean_text_joins_broken_lines():
    raw = "Artificial Intelligence\n      is transforming\nhealthcare."
    result = clean_text(raw)
    assert result == "Artificial Intelligence is transforming healthcare."


def test_clean_text_removes_page_numbers():
    raw = "Some content.\n3\nMore content."
    result = clean_text(raw)
    assert "3" not in result.split()


def test_clean_text_collapses_multiple_spaces():
    raw = "Too    many     spaces."
    result = clean_text(raw)
    assert result == "Too many spaces."


def test_clean_text_removes_special_characters():
    raw = "Weird@@ chars### here!!"
    result = clean_text(raw)
    assert "@" not in result
    assert "#" not in result


def test_clean_text_preserves_paragraph_breaks():
    raw = "Paragraph one.\n\nParagraph two."
    result = clean_text(raw)
    assert result == "Paragraph one.\n\nParagraph two."


def test_clean_text_empty_input():
    assert clean_text("") == ""