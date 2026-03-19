"""
Text processing utilities for Smart Resume Analyzer
"""

import io
import re
import os
import tempfile
import pdfplumber
import docx2txt
import nltk
from nltk.corpus import stopwords
import streamlit as st

# Download NLTK data if needed
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
try:
    nltk.data.find('taggers/averaged_perceptron_tagger_eng')
except LookupError:
    nltk.download('averaged_perceptron_tagger_eng', quiet=True)

def extract_text_from_pdf(file_bytes: bytes) -> str:
    text_parts = []
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                txt = page.extract_text() or ""
                text_parts.append(txt)
    except Exception as e:
        return ""
    return "\n".join(text_parts)

def extract_text_from_docx(file_bytes: bytes) -> str:
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
            tmp.write(file_bytes)
            tmp.flush()
            tmp_path = tmp.name
        txt = docx2txt.process(tmp_path) or ""
        return txt
    except Exception:
        return ""
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass

def extract_text_from_file(uploaded) -> str:
    """Detect type and extract text"""
    try:
        content = uploaded.read()
        name = uploaded.name.lower()
        if name.endswith(".pdf"):
            return extract_text_from_pdf(content)
        if name.endswith(".docx") or name.endswith(".doc"):
            return extract_text_from_docx(content)
        # fallback: treat as text
        try:
            return content.decode("utf-8")
        except Exception:
            try:
                return content.decode("latin-1")
            except Exception:
                return ""
    except Exception:
        return ""

def clean_text(s: str) -> str:
    # simple cleaning for parsing
    s = str(s)
    s = re.sub(r"\r", "\n", s)
    s = re.sub(r"\s+\n", "\n", s)
    s = re.sub(r"\n{2,}", "\n\n", s)
    s = s.strip()
    return s

def count_action_verbs(resume_text: str) -> int:
    try:
        tokens = nltk.word_tokenize(resume_text)
        pos_tags = nltk.pos_tag(tokens)
        # Count unique verbs (approximate, NLTK tags start with VB for verbs)
        verbs = [word.lower() for word, pos in pos_tags if pos.startswith('VB')]
        return len(set(verbs))
    except Exception:
        return 0
