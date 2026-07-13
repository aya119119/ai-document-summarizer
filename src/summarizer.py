"""
summarizer.py

Wires the full pipeline together: read -> clean -> tokenize -> embed ->
cluster -> select representative sentences. This is the single entry
point the Streamlit app (or anything else) should call.
"""

from src.document_reader import read_document
from src.preprocessing import clean_text
from src.nlp_pipeline import split_sentences, process_text
from src.embeddings import train_word_vectors, build_sentence_vectors
from src.clustering import select_representative_sentences


def summarize_text(text: str, num_sentences: int = 3) -> str:
    """
    Run the full extractive summarization pipeline on raw text.

    Args:
        text: Raw text (as extracted from a document, unprocessed).
        num_sentences: Desired number of sentences in the summary.

    Returns:
        The summary as a single string (selected sentences joined by
        a space), in their original order of appearance.
    """
    cleaned = clean_text(text)

    sentences = split_sentences(cleaned)
    if not sentences:
        return ""

    # If the document is shorter than the requested summary length,
    # just return the whole thing.
    if len(sentences) <= num_sentences:
        return " ".join(sentences)

    tokenized_sentences = process_text(cleaned)
    model = train_word_vectors(tokenized_sentences)
    sentence_vectors = build_sentence_vectors(tokenized_sentences, model)

    summary_sentences = select_representative_sentences(
        sentences, sentence_vectors, num_clusters=num_sentences
    )

    return " ".join(summary_sentences)


def summarize_document(file_path: str, num_sentences: int = 3) -> str:
    """
    Read a document from disk and summarize it.

    Args:
        file_path: Path to a .pdf, .docx, or .txt file.
        num_sentences: Desired number of sentences in the summary.

    Returns:
        The summary as a single string.
    """
    raw_text = read_document(file_path)
    return summarize_text(raw_text, num_sentences=num_sentences)


def get_document_stats(text: str, summary: str) -> dict:
    """
    Compute basic statistics comparing the original text to its summary.

    Args:
        text: The raw original text.
        summary: The generated summary.

    Returns:
        A dict with word/sentence counts and compression ratio.
    """
    original_sentences = split_sentences(clean_text(text))
    summary_sentences = split_sentences(summary)

    original_word_count = len(text.split())
    summary_word_count = len(summary.split())

    compression_ratio = (
        round(1 - (summary_word_count / original_word_count), 2)
        if original_word_count
        else 0.0
    )

    return {
        "original_word_count": original_word_count,
        "summary_word_count": summary_word_count,
        "original_sentence_count": len(original_sentences),
        "summary_sentence_count": len(summary_sentences),
        "compression_ratio": compression_ratio,
    }