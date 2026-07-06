"""
Tests for src/document_reader.py
"""

import pytest

from src.document_reader import read_document, UnsupportedFileTypeError


def test_read_txt(tmp_path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("Hello world.")

    result = read_document(str(file_path))

    assert result == "Hello world."


def test_read_document_missing_file():
    with pytest.raises(FileNotFoundError):
        read_document("does_not_exist.txt")


def test_read_document_unsupported_type(tmp_path):
    file_path = tmp_path / "sample.xyz"
    file_path.write_text("irrelevant")

    with pytest.raises(UnsupportedFileTypeError):
        read_document(str(file_path))