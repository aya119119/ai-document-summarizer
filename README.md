#  Document Summarizer

A Python-based document summarization application that extracts the most important information from **PDF**, **Word (.docx)**, and **TXT** files using **Natural Language Processing (NLP)** and **Machine Learning** techniques.

The application features an interactive **Streamlit** interface, allowing users to upload documents, generate summaries, view document statistics, and download the generated summary.

---

##  Features

-  Supports multiple document formats
  - PDF
  - Word (.docx)
  - TXT
-  Automatic text cleaning and preprocessing
-  NLP pipeline
  - Tokenization
  - Stop-word removal
  - Stemming/Lemmatization
-  Word Embeddings for sentence representation
-  K-Means clustering to identify important sentences
-  Extractive text summarization
-  Interactive Streamlit web interface
-  Download generated summaries
-  Document statistics

---

#  How It Works

The summarization process follows several stages.

## 1. Document Reading

The application accepts three file formats:

- PDF
- DOCX
- TXT

Different libraries are used depending on the document type.

| Format | Libraries |
|---------|-----------|
| PDF | PyMuPDF, pdfplumber, PyPDF2 |
| DOCX | python-docx |
| TXT | Built-in Python functions |

After reading the file, the content is converted into a single plain-text string.

---

## 2. Text Preprocessing

Raw documents often contain unwanted elements such as:

- Extra spaces
- Blank lines
- Page numbers
- Line breaks
- References
- Special characters

The preprocessing stage cleans the text to improve summarization quality.

### Example

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

---

## 3. Natural Language Processing (NLP)

The cleaned text is processed using NLP techniques.

The pipeline includes:

- Sentence tokenization
- Word tokenization
- Stop-word removal
- Punctuation removal
- Stemming or Lemmatization

### Example

Original sentence

```
The cat is sitting on the table.
```

Processed

```
cat sitting table
```

Words sharing the same meaning are normalized.

Example

```
running
runs
ran
```

↓

```
run
```

---

## 4. Text Representation

Computers cannot process words directly.

Each word is transformed into a numerical vector using **Word Embeddings**.

Supported embedding techniques include:

- Word2Vec
- GloVe
- FastText

Example

```
dog

↓

[0.41, 0.22, ..., 300 dimensions]
```

Sentence vectors are then created from these word embeddings.

---

## 5. Sentence Importance Detection

Each sentence is represented as a vector.

The vectors are grouped using **K-Means Clustering**.

Each cluster represents a different topic in the document.

The sentence closest to the centroid of each cluster is selected as the representative sentence.

---

## 6. Summary Generation

The application performs **Extractive Summarization**.

Instead of generating new text, it selects the most informative sentences directly from the original document.

Example

Original document

```
Sentence 1
Sentence 2
Sentence 3
Sentence 4
Sentence 5
```

Generated summary

```
Sentence 2
Sentence 5
```

---

## 7. User Interface

The application provides a simple interface built with **Streamlit**.

Workflow:

1. Upload a document
2. Click **Summarize**
3. View the extracted summary
4. Review document statistics
5. Download the generated summary

---

