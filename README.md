# Document Summarizer

A Python-based document summarization dashboard that will extract the most important information from **PDF**, **Word (.docx)**, and **TXT** files using **Natural Language Processing (NLP)** and **Machine Learning** techniques.

Using a **Streamlit** interface, allowing users to upload documents, generate summaries, view document statistics, and download the generated summary.

> **Status:**  Work in progress.

---

## Planned Features

- [ ] Support for multiple document formats
  - [ ] PDF
  - [ ] Word (.docx)
  - [ ] TXT
- [ ] Automatic text cleaning and preprocessing
- [ ] NLP pipeline
  - [ ] Tokenization
  - [ ] Stop-word removal
  - [ ] Stemming/Lemmatization
- [ ] Word embeddings for sentence representation
- [ ] K-Means clustering to identify important sentences
- [ ] Extractive text summarization
- [ ] Interactive Streamlit web interface
- [ ] Downloadable summaries
- [ ] Document statistics

---

## How It Will Work

The summarization pipeline will follow several stages.

### 1. Document Reading

The application will accept three file formats:

- PDF
- DOCX
- TXT

Different libraries will be used depending on the document type.

| Format | Libraries |
|---------|-----------|
| PDF | PyMuPDF, pdfplumber, PyPDF2 |
| DOCX | python-docx |
| TXT | Built-in Python functions |

After reading a file, its content will be converted into a single plain-text string.

---

### 2. Text Preprocessing

Raw documents often contain unwanted elements such as:

- Extra spaces
- Blank lines
- Page numbers
- Line breaks
- References
- Special characters

The preprocessing stage will clean the text to improve summarization quality.

**Example**

Before:
```
Artificial Intelligence
      is transforming
healthcare.
```

After:
```
Artificial Intelligence is transforming healthcare.
```

---

### 3. Natural Language Processing (NLP)

The cleaned text will be processed using NLP techniques. The pipeline will include:

- Sentence tokenization
- Word tokenization
- Stop-word removal
- Punctuation removal
- Stemming or lemmatization

**Example**

Original sentence:
```
The cat is sitting on the table.
```

Processed:
```
cat sitting table
```

Words sharing the same meaning will be normalized, e.g. `running`, `runs`, `ran` → `run`.

---

### 4. Text Representation

Each word will be transformed into a numerical vector using word embeddings. Supported techniques will include:

- Word2Vec
- GloVe
- FastText

Sentence vectors will then be built from these word embeddings.

---

### 5. Sentence Importance Detection

Each sentence will be represented as a vector. The vectors will be grouped using **K-Means Clustering**, where each cluster represents a different topic in the document. The sentence closest to each cluster's centroid will be selected as the representative sentence.

---

### 6. Summary Generation

The application will perform **extractive summarization** — selecting the most informative sentences directly from the original document rather than generating new text.

---

### 7. User Interface

The application will provide a simple interface built with **Streamlit**.

Planned workflow:

1. Upload a document
2. Click **Summarize**
3. View the extracted summary
4. Review document statistics
5. Download the generated summary

---

## Project Structure

```
document-summarizer/
├── README.md
├── requirements.txt
├── app.py
├── src/
│   ├── document_reader.py
│   ├── preprocessing.py
│   ├── nlp_pipeline.py
│   ├── embeddings.py
│   ├── clustering.py
│   └── summarizer.py
└── tests/
```

## Setup (once dependencies are added)

```bash
pip install -r requirements.txt
streamlit run app.py
```
