"""
app.py

Streamlit interface for the Document Summarizer.
Notion-inspired UI using a warm cream / deep navy / crimson palette.

Workflow:
    1. Upload a document (PDF, DOCX, or TXT)
    2. Click "Summarize"
    3. View the extracted summary as callout cards
    4. Review document statistics
    5. Download the generated summary
"""

import tempfile
from pathlib import Path

import streamlit as st

from src.document_reader import read_document, UnsupportedFileTypeError
from src.summarizer import summarize_text, get_document_stats
from src.nlp_pipeline import split_sentences


st.set_page_config(page_title="Document Summarizer", page_icon="📄", layout="centered")

# ---------------------------------------------------------------------------
# Design tokens + custom styling
# ---------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@500&display=swap');

:root {
    --bg: #FDF0D5;
    --surface: #FFFFFF;
    --surface-alt: #FBEEDB;
    --text-primary: #003049;
    --text-secondary: #4d6478;
    --accent-crimson: #C1121F;
    --accent-deep: #780000;
    --accent-blue: #669BBC;
    --border: rgba(0, 48, 73, 0.10);
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: var(--text-primary);
}

.stApp {
    background-color: var(--bg);
}

.block-container {
    max-width: 760px;
    padding-top: 3rem;
    padding-bottom: 4rem;
}

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] {
    background-color: var(--text-primary);
    border-right: none;
}
[data-testid="stSidebar"] * {
    color: var(--bg) !important;
}
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] p {
    opacity: 0.85;
}
[data-testid="stSidebar"] hr {
    border-color: rgba(253, 240, 213, 0.15);
}

/* Sidebar eyebrow label */
.sidebar-eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--accent-blue) !important;
    margin-bottom: 0.25rem;
}

/* ---------- Header ---------- */
.eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--accent-crimson);
    margin-bottom: 0.6rem;
}

.hero-title {
    font-family: 'Fraunces', serif;
    font-weight: 600;
    font-size: 2.6rem;
    line-height: 1.15;
    color: var(--text-primary);
    margin-bottom: 0.6rem;
}

.hero-subtitle {
    font-family: 'Inter', sans-serif;
    font-size: 1rem;
    color: var(--text-secondary);
    max-width: 46ch;
    margin-bottom: 2.5rem;
}

/* ---------- Section labels ---------- */
.section-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--accent-deep);
    margin: 2.2rem 0 0.9rem 0;
}

/* ---------- Callout cards (summary sentences) ---------- */
.callout-card {
    background-color: var(--surface);
    border-left: 4px solid var(--accent-crimson);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.75rem;
    box-shadow: 0 1px 3px rgba(0, 48, 73, 0.06);
    font-size: 0.98rem;
    line-height: 1.55;
    color: var(--text-primary);
}
.callout-card.accent-deep { border-left-color: var(--accent-deep); }
.callout-card.accent-blue { border-left-color: var(--accent-blue); }

/* ---------- Stat chips ---------- */
.stat-row {
    display: flex;
    gap: 0.6rem;
    flex-wrap: wrap;
    margin-bottom: 1.5rem;
}
.stat-chip {
    background-color: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.7rem 1rem;
    flex: 1;
    min-width: 130px;
}
.stat-chip .stat-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.3rem;
    font-weight: 500;
    color: var(--accent-deep);
}
.stat-chip .stat-label {
    font-family: 'Inter', sans-serif;
    font-size: 0.72rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-top: 0.15rem;
}

/* ---------- Empty state ---------- */
.empty-state {
    background-color: var(--surface-alt);
    border: 1px dashed var(--border);
    border-radius: 12px;
    padding: 2rem;
    text-align: center;
    color: var(--text-secondary);
    font-size: 0.95rem;
}

/* ---------- Buttons ---------- */
.stButton > button {
    background-color: var(--accent-crimson);
    color: var(--bg);
    border: none;
    border-radius: 8px;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    padding: 0.55rem 1.4rem;
}
.stButton > button:hover {
    background-color: var(--accent-deep);
    color: var(--bg);
}
[data-testid="stSidebar"] .stButton > button {
    background-color: var(--accent-crimson);
    color: var(--bg) !important;
    width: 100%;
}
.stDownloadButton > button {
    background-color: var(--text-primary);
    color: var(--bg);
    border: none;
    border-radius: 8px;
    font-weight: 600;
}
.stDownloadButton > button:hover {
    background-color: var(--accent-crimson);
    color: var(--bg);
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Sidebar: upload + controls
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="sidebar-eyebrow">Document Summarizer</div>', unsafe_allow_html=True)
    st.markdown("### Upload")
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt"], label_visibility="collapsed")

    st.markdown("### Summary length")
    num_sentences = st.slider("Sentences", min_value=1, max_value=10, value=3, label_visibility="collapsed")

    st.markdown("---")
    summarize_clicked = st.button("Summarize", use_container_width=True, disabled=uploaded_file is None)

# ---------------------------------------------------------------------------
# Main content
# ---------------------------------------------------------------------------
st.markdown('<div class="eyebrow">PDF · DOCX · TXT</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">Read less.<br>Know more.</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-subtitle">Upload a document and get an extractive summary '
    "built with NLP, word embeddings, and clustering — the key sentences, "
    "pulled straight from your source.</div>",
    unsafe_allow_html=True,
)

ACCENT_CLASSES = ["", "accent-deep", "accent-blue"]

if uploaded_file is None:
    st.markdown(
        '<div class="empty-state">Upload a document from the sidebar to get started.</div>',
        unsafe_allow_html=True,
    )
elif summarize_clicked:
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

    st.markdown('<div class="section-label">Statistics</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="stat-row">
            <div class="stat-chip"><div class="stat-value">{stats['original_word_count']}</div><div class="stat-label">Original words</div></div>
            <div class="stat-chip"><div class="stat-value">{stats['summary_word_count']}</div><div class="stat-label">Summary words</div></div>
            <div class="stat-chip"><div class="stat-value">{stats['compression_ratio'] * 100:.0f}%</div><div class="stat-label">Compression</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-label">Summary</div>', unsafe_allow_html=True)

    if summary:
        for i, sentence in enumerate(split_sentences(summary)):
            accent = ACCENT_CLASSES[i % len(ACCENT_CLASSES)]
            st.markdown(
                f'<div class="callout-card {accent}">{sentence}</div>',
                unsafe_allow_html=True,
            )

        st.download_button(
            label="Download summary",
            data=summary,
            file_name=f"{Path(uploaded_file.name).stem}_summary.txt",
            mime="text/plain",
        )
    else:
        st.markdown(
            '<div class="empty-state">No summary could be generated.</div>',
            unsafe_allow_html=True,
        )
else:
    st.markdown(
        '<div class="empty-state">File ready — click <strong>Summarize</strong> in the sidebar.</div>',
        unsafe_allow_html=True,
    )