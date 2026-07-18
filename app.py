"""
app.py

Streamlit interface for the Document Summarizer.

Workflow:
    1. Upload a document (PDF, DOCX, or TXT)
    2. Click "Summarize"
    3. View the extracted summary
    4. Review document statistics
    5. Download the generated summary
"""

import tempfile
from pathlib import Path

import streamlit as st

from src.document_reader import read_document, UnsupportedFileTypeError
from src.summarizer import summarize_text, get_document_stats


st.set_page_config(page_title="Document Summarizer", page_icon="📄", layout="centered")

st.title("📄 Document Summarizer")
st.write(
    "Upload a PDF, Word (.docx), or TXT file and get an extractive summary "
    "built with NLP, word embeddings, and clustering."
)

uploaded_file = st.file_uploader(
    "Upload a document", type=["pdf", "docx", "txt"]
)

num_sentences = st.slider(
    "Number of sentences in the summary", min_value=1, max_value=10, value=3
)

if uploaded_file is not None:
    if st.button("Summarize"):
        tmp_path = None
        try:
            with st.spinner("Reading and summarizing document..."):
                suffix = Path(uploaded_file.name).suffix
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name

                raw_text = read_document(tmp_path)

                if not raw_text.strip():
                    st.warning("This document appears to be empty or unreadable.")
                    st.stop()

                summary = summarize_text(raw_text, num_sentences=num_sentences)
                stats = get_document_stats(raw_text, summary)

        except UnsupportedFileTypeError:
            st.error("This file type isn't supported. Please upload a PDF, DOCX, or TXT file.")
            st.stop()
        except FileNotFoundError:
            st.error("The uploaded file could not be read. Please try uploading it again.")
            st.stop()
        except Exception as e:
            st.error(f"Something went wrong while summarizing this document: {e}")
            st.stop()
        finally:
            if tmp_path:
                Path(tmp_path).unlink(missing_ok=True)

        st.subheader("Summary")
        st.write(summary if summary else "_No summary could be generated._")

        st.subheader("Document Statistics")
        col1, col2, col3 = st.columns(3)
        col1.metric("Original words", stats["original_word_count"])
        col2.metric("Summary words", stats["summary_word_count"])
        col3.metric("Compression", f"{stats['compression_ratio'] * 100:.0f}%")

        col4, col5 = st.columns(2)
        col4.metric("Original sentences", stats["original_sentence_count"])
        col5.metric("Summary sentences", stats["summary_sentence_count"])

        if summary:
            st.download_button(
                label="Download summary",
                data=summary,
                file_name=f"{Path(uploaded_file.name).stem}_summary.txt",
                mime="text/plain",
            )
else:
    st.info("Upload a document to get started.")