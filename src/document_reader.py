"""
document_reader.py

Reads PDF, DOCX, and TXT files and returns their raw text content
as a single plain-text string.
"""

from pathlib import Path

import fitz  # PyMuPDF
from docx import Document


class UnsupportedFileTypeError(Exception):
    """Raised when a file extension is not supported."""


def read_document(file_path: str) -> str:
    """
    Read a document and return its content as plain text.

    Supports .pdf, .docx, and .txt files.

    Args:
        file_path: Path to the document.

    Returns:
        The extracted text content of the document.

    Raises:
        FileNotFoundError: If the file does not exist.
        UnsupportedFileTypeError: If the file extension is not supported.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    suffix = path.suffix.lower()

    if suffix == ".pdf":
        return _read_pdf(path)
    elif suffix == ".docx":
        return _read_docx(path)
    elif suffix == ".txt":
        return _read_txt(path)
    else:
        raise UnsupportedFileTypeError(
            f"Unsupported file type '{suffix}'. Supported types: .pdf, .docx, .txt"
        )


def _read_pdf(path: Path) -> str:
    """Extract text from a PDF file using PyMuPDF."""
    text_parts = []
    with fitz.open(path) as pdf:
        for page in pdf:
            text_parts.append(page.get_text())
    return "\n".join(text_parts)


def _read_docx(path: Path) -> str:
    """Extract text from a DOCX file using python-docx."""
    document = Document(path)
    paragraphs = [paragraph.text for paragraph in document.paragraphs]
    return "\n".join(paragraphs)


def _read_txt(path: Path) -> str:
    """Read text from a plain TXT file."""
    return path.read_text(encoding="utf-8", errors="ignore")