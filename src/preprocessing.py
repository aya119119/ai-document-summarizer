"""
preprocessing.py

Cleans raw text extracted from a document before it is fed into the NLP pipeline.

Handles common artifacts found in extracted documents:
- Extra whitespace and blank lines
- Line breaks that split sentences mid-thought
- Page numbers
- Special / non-printable characters
"""

import re


_PAGE_NUMBER_PATTERN = re.compile(r"^\s*\d+\s*$", re.MULTILINE)
_SPECIAL_CHARS_PATTERN = re.compile(r"[^\w\s.,!?;:'\"()\-]")
_MULTIPLE_SPACES_PATTERN = re.compile(r"[ \t]+")
_MULTIPLE_NEWLINES_PATTERN = re.compile(r"\n\s*\n+")


def clean_text(text: str) -> str:
    """
    Clean raw text extracted from a document.

    Args:
        text: Raw text, possibly containing extra whitespace, page
            numbers, stray line breaks, and special characters.

    Returns:
        A single cleaned string suitable for sentence tokenization.
    """
    if not text:
        return ""

    text = _remove_page_numbers(text)
    text = _join_line_breaks(text)
    text = _remove_special_characters(text)
    text = _normalize_whitespace(text)

    return text.strip()


def _remove_page_numbers(text: str) -> str:
    """Remove lines that consist of only a number (typical page numbers)."""
    return _PAGE_NUMBER_PATTERN.sub("", text)


def _join_line_breaks(text: str) -> str:
    """
    Join lines that were broken mid-sentence (e.g. by a PDF layout)
    into a single line, while preserving paragraph breaks (blank lines).
    """
    paragraphs = _MULTIPLE_NEWLINES_PATTERN.split(text)
    joined_paragraphs = []

    for paragraph in paragraphs:
        lines = [line.strip() for line in paragraph.splitlines()]
        lines = [line for line in lines if line]
        joined_paragraphs.append(" ".join(lines))

    return "\n\n".join(p for p in joined_paragraphs if p)


def _remove_special_characters(text: str) -> str:
    """Strip characters that aren't letters, digits, whitespace, or basic punctuation."""
    return _SPECIAL_CHARS_PATTERN.sub("", text)


def _normalize_whitespace(text: str) -> str:
    """Collapse repeated spaces/tabs, keeping paragraph breaks intact."""
    text = _MULTIPLE_SPACES_PATTERN.sub(" ", text)
    return text