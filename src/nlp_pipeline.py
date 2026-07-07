"""
nlp_pipeline.py

Turns cleaned text into normalized tokens ready for embedding.

Pipeline stages:
1. Sentence tokenization
2. Word tokenization
3. Stop-word removal
4. Punctuation removal
5. Stemming
"""

import string

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize


def _ensure_nltk_data() -> None:
    """Download required NLTK resources if they aren't already present."""
    resources = [
        ("tokenizers/punkt", "punkt"),
        ("tokenizers/punkt_tab", "punkt_tab"),
        ("corpora/stopwords", "stopwords"),
    ]
    for path, package in resources:
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(package, quiet=True)


_ensure_nltk_data()

_STOPWORDS = set(stopwords.words("english"))
_PUNCTUATION = set(string.punctuation)
_stemmer = PorterStemmer()


def split_sentences(text: str) -> list[str]:
    """Split cleaned text into a list of sentences."""
    if not text:
        return []
    return sent_tokenize(text)


def process_sentence(sentence: str) -> list[str]:
    """
    Tokenize a single sentence into normalized, content-bearing words.

    Applies word tokenization, punctuation removal, stop-word removal,
    and stemming, in that order.

    Args:
        sentence: A single sentence of cleaned text.

    Returns:
        A list of stemmed, lowercased content words.
    """
    tokens = word_tokenize(sentence)
    tokens = [token.lower() for token in tokens if token not in _PUNCTUATION]
    tokens = [token for token in tokens if token not in _STOPWORDS]
    tokens = [_stemmer.stem(token) for token in tokens if token.isalpha()]
    return tokens


def process_text(text: str) -> list[list[str]]:
    """
    Run the full NLP pipeline on cleaned text.

    Args:
        text: Cleaned text (see src.preprocessing.clean_text).

    Returns:
        A list where each element is the list of processed tokens
        for the corresponding sentence in the text.
    """
    sentences = split_sentences(text)
    return [process_sentence(sentence) for sentence in sentences]