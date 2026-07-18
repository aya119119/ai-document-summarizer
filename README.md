# Document Summarizer

A Python-based document summarization application that extracts the most important information from **PDF**, **Word (.docx)**, and **TXT** files using **Natural Language Processing (NLP)** and **Machine Learning** techniques.

The application features an interactive **Streamlit** interface, allowing users to upload documents, generate summaries, view document statistics, and download the generated summary.

---

## Features

- [x] Support for multiple document formats
  - [x] PDF
  - [x] Word (.docx)
  - [x] TXT
- [x] Automatic text cleaning and preprocessing
- [x] NLP pipeline
  - [x] Tokenization
  - [x] Stop-word removal
  - [x] Stemming
- [x] Word embeddings for sentence representation (Word2Vec)
- [x] K-Means clustering to identify important sentences
- [x] Extractive text summarization
- [x] Interactive Streamlit web interface
- [x] Downloadable summaries
- [x] Document statistics

---

## How It Works

The summarization pipeline runs in seven stages.

### 1. Document Reading (`src/document_reader.py`)

Reads PDF, DOCX, and TXT files and converts their content into a single plain-text string.

| Format | Library |
|---------|---------|
| PDF | PyMuPDF |
| DOCX | python-docx |
| TXT | Built-in Python functions |

### 2. Text Preprocessing (`src/preprocessing.py`)

Cleans raw text by removing page numbers, joining broken lines, stripping unnecessary characters, and collapsing extra whitespace.

**Example**

**Before**
```
Artificial Intelligence
is transforming
healthcare.
```

**After**
```
Artificial Intelligence is transforming healthcare.
```

### 3. NLP Pipeline (`src/nlp_pipeline.py`)

Splits cleaned text into sentences, then tokenizes, removes stop words and punctuation, and stems each word.

**Example**

**Input**
```
The cat is sitting on the table.
```

**Processed**
```
cat sit tabl
```

### 4. Word Embeddings (`src/embeddings.py`)

A Word2Vec model is trained on the document's own tokens, and each sentence is represented as the average of its word vectors.

### 5. Sentence Importance Detection (`src/clustering.py`)

Sentence vectors are grouped using **K-Means clustering**. Each cluster represents a topic in the document, and the sentence closest to each cluster's centroid is selected as that topic's representative sentence.

### 6. Summary Generation (`src/summarizer.py`)

Combines every stage above into a single function, `summarize_text()`, which returns the final extractive summary along with document statistics.

### 7. User Interface (`app.py`)

The Streamlit application allows users to:

1. Upload a document.
2. Choose the number of sentences for the summary.
3. Click **Summarize**.
4. View the generated summary and document statistics.
5. Download the summary as a text file.

---

## Project Structure

```text
document-summarizer/
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── app.py
├── src/
│   ├── __init__.py
│   ├── document_reader.py
│   ├── preprocessing.py
│   ├── nlp_pipeline.py
│   ├── embeddings.py
│   ├── clustering.py
│   └── summarizer.py
└── tests/
    ├── __init__.py
    ├── test_document_reader.py
    ├── test_preprocessing.py
    ├── test_nlp_pipeline.py
    ├── test_embeddings.py
    ├── test_clustering.py
    └── test_summarizer.py
```

---

## Setup

Install the project dependencies:

```bash
pip install -r requirements.txt
```

---

## Run the App

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser at:

```
http://localhost:8501
```

---

## Run the Tests

Run the complete test suite:

```bash
python -m pytest tests/ -v
```

All **26 tests** should pass, covering every stage of the summarization pipeline.

---

## Tech Stack

- Python
- Streamlit
- PyMuPDF
- python-docx
- NLTK
- Gensim (Word2Vec)
- scikit-learn
- NumPy
- pytest