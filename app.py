"""
Smart Resume Analyzer
======================
An AI-powered resume analysis tool that helps optimize resumes for ATS systems.

Author: NFS Programming
GitHub: https://github.com/nfsprogramming
Repository: https://github.com/nfsprogramming/smartresumeanlyzer
Year: 2026

Features:
- Resume parsing (PDF, DOCX, TXT)
- AI-powered semantic analysis
- Skill matching and gap analysis
- Keyword extraction from job descriptions
- Actionable recommendations
- Premium dark theme UI

License: MIT
"""

import os
import io
import re
import tempfile
from typing import List, Tuple
import streamlit as st
import pandas as pd
import pdfplumber
import docx2txt
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer, util
import nltk
import ssl

# Handle SSL certificate issues in cloud environments
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Ensure NLTK data available - robust download for Streamlit Cloud
def ensure_nltk_data():
    """Download NLTK data if not present."""
    datasets = [
        ('tokenizers/punkt', 'punkt'),
        ('tokenizers/punkt_tab', 'punkt_tab'),
        ('taggers/averaged_perceptron_tagger_eng', 'averaged_perceptron_tagger_eng'),
    ]
    
    for path, name in datasets:
        try:
            nltk.data.find(path)
        except LookupError:
            try:
                nltk.download(name, quiet=True)
            except Exception as e:
                print(f"Warning: Failed to download {name}: {e}")

# Download NLTK data at startup
ensure_nltk_data()

# Load a small semantic model for efficient performance
@st.cache_resource
def load_sentence_transformer():
    return SentenceTransformer("all-MiniLM-L6-v2")

EMBED_MODEL = load_sentence_transformer()



# ---------------- Utility functions ----------------
def extract_text_from_pdf(file_bytes: bytes) -> str:
    text_parts = []
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                txt = page.extract_text() or ""
                text_parts.append(txt)
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""
    return "\n".join(text_parts)

def extract_text_from_docx(file_bytes: bytes) -> str:
    # Use delete=False for compatibility, then manually remove
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
            tmp.write(file_bytes)
            tmp.flush()
            tmp_path = tmp.name
        txt = docx2txt.process(tmp_path) or ""
        return txt
    except Exception as e:
        st.error(f"Error reading DOCX: {e}")
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
    except Exception as e:
        st.error(f"Error processing file: {e}")
        return ""

def clean_text(s: str) -> str:
    # simple cleaning for parsing
    s = str(s)
    s = re.sub(r"\r", "\n", s)
    s = re.sub(r"\s+\n", "\n", s)
    s = re.sub(r"\n{2,}", "\n\n", s)
    s = s.strip()
    return s

def extract_top_keywords(jd_text: str, top_k=10) -> List[str]:
    if not jd_text or not jd_text.strip():
        return []
    # Use TF-IDF to pick top keywords/phrases (unigrams + bigrams)
    try:
        vec = TfidfVectorizer(stop_words="english", ngram_range=(1,2), max_features=200)
        X = vec.fit_transform([jd_text])
        feature_array = vec.get_feature_names_out()
        tfidf_scores = X.toarray()[0]
        top_indices = tfidf_scores.argsort()[::-1][:top_k]
        keywords = [feature_array[i] for i in top_indices if tfidf_scores[i] > 0]
        return keywords
    except ValueError:
        return []

COMMON_SKILLS = [
    # short list — expand as needed
    "python","java","c++","c#","javascript","react","node.js","sql","nosql",
    "mongodb","postgresql","aws","azure","gcp","docker","kubernetes","linux",
    "git","nlp","computer vision","machine learning","deep learning","pandas",
    "numpy","tensorflow","pytorch","scikit-learn","data analysis","excel",
    "communication","problem solving","teamwork","leadership","sql server",
    "html", "css", "flask", "django", "fastapi", "rest api", "graphql",
    "agile", "scrum", "project management", "devops", "ci/cd"
]

def match_skills(resume_text: str, skills_list=COMMON_SKILLS) -> Tuple[List[str], List[str]]:
    rt = resume_text.lower()
    found = []
    missing = []
    for s in skills_list:
        # Improved matching: prevent partial matches (e.g. 'java' in 'javascript')
        # This was already handled by \b, but let's be sure.
        if re.search(r"\b" + re.escape(s.lower()) + r"\b", rt):
            found.append(s)
        else:
            missing.append(s)
    return found, missing

def semantic_similarity(a: str, b: str) -> float:
    # Returns cosine similarity in [0,1]
    emb_a = EMBED_MODEL.encode(a, convert_to_tensor=True)
    emb_b = EMBED_MODEL.encode(b, convert_to_tensor=True)
    sim = util.cos_sim(emb_a, emb_b).item()
    # convert -1..1 to 0..1 (though cosine sim with this model is usually 0..1)
    return max(0.0, min(1.0, float(sim)))

def count_action_verbs(resume_text: str) -> int:
    tokens = nltk.word_tokenize(resume_text)
    pos_tags = nltk.pos_tag(tokens)
    # Count unique verbs (approximate, NLTK tags start with VB for verbs)
    verbs = [word.lower() for word, pos in pos_tags if pos.startswith('VB')]
    return len(set(verbs))

def generate_recommendations(resume_text: str, jd_text: str, keywords: List[str], found_skills: List[str], missing_skills: List[str], sim_score: float) -> List[str]:
    recs = []
    # keyword suggestions
    missing_keywords = [k for k in keywords if not re.search(r"\b" + re.escape(k) + r"\b", resume_text, flags=re.I)]
    if missing_keywords:
        recs.append(f"Include these important keywords from the job description: {', '.join(missing_keywords[:8])}")
    # skills
    if missing_skills:
        recs.append(f"Consider adding relevant skills missing from resume (examples): {', '.join(missing_skills[:8])}")
    # metrics suggestion
    if "0" or "percent" not in resume_text.lower():
        recs.append("Add quantifiable achievements where possible (e.g., 'Improved X by 30%').")
    # action verbs
    av = count_action_verbs(resume_text)
    if av < 5:
        recs.append("Use more action verbs (designed, improved, led, implemented) to describe accomplishments.")
    # similarity
    if sim_score < 0.55:
        recs.append("Overall fit appears low → tailor your resume to the JD: reorder top skills and summary to match.")
    else:
        recs.append("Good semantic match to the job description — highlight the top matching skills near the top of the resume.")
    return recs

# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="Smart Resume Analyzer", page_icon="🧾", layout="wide")

# Custom CSS for a premium feel
st.markdown("""
<style>
    /* Global App Background - Deep Black */
    .stApp {
        background: radial-gradient(circle at center, #141414, #000000);
        color: #e0e0e0;
    }
    
    /* Card Glassmorphism - Dark with Gold accents */
    .stCard {
        background-color: rgba(20, 20, 25, 0.7);
        padding: 25px;
        border-radius: 12px;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 215, 0, 0.2); /* Subtle Gold Border */
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
    }
    
    /* Headings - Gold */
    h1, h2, h3 {
        font-family: 'Courier New', Courier, monospace !important;
        font-weight: 700;
        color: #FFD700 !important; /* Gold */
        text-shadow: 0 0 10px rgba(255, 215, 0, 0.2);
    }
    
    /* Metric Values - Neon Blue for contrast */
    .metric-value {
        font-size: 2.2rem !important;
        font-weight: 800;
        color: #00BFFF !important; /* Deep Sky Blue */
        text-shadow: 0 0 15px rgba(0, 191, 255, 0.3);
    }
    
    /* Buttons - Gradient Gold */
    .stButton>button {
        background: linear-gradient(135deg, #B8860B 0%, #FFD700 100%);
        color: #000000;
        border: none;
        padding: 12px 28px;
        border-radius: 6px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.2);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.4);
        color: #000000;
    }
    
    /* Input Fields */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #1a1a1a;
        color: #ffffff;
        border: 1px solid #333;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #FFD700;
        box-shadow: 0 0 5px rgba(255, 215, 0, 0.5);
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    ::-webkit-scrollbar-track {
        background: #000; 
    }
    ::-webkit-scrollbar-thumb {
        background: #333; 
        border-radius: 5px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #FFD700; 
    }
</style>
""", unsafe_allow_html=True)

st.title("🧾 Smart Resume Analyzer")
st.markdown("**Optimize your resume for Applicant Tracking Systems (ATS) with AI-powered insights.**")
st.markdown("""
<div style="text-align: center; margin-bottom: 20px;">
    <p style="color: #888; font-size: 0.9rem;">
        Developed by <strong style="color: #FFD700;">NFS Programming</strong> | 
        <a href="https://github.com/nfsprogramming" target="_blank" style="color: #00BFFF; text-decoration: none;">GitHub</a>
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1,1])

with col1:
    st.markdown("### 1) Upload Resume")
    uploaded_resume = st.file_uploader("Upload PDF / DOCX / TXT", type=["pdf","docx","doc","txt"])
    if uploaded_resume:
        st.success(f"File uploaded: {uploaded_resume.name}")

with col2:
    st.markdown("### 2) Job Description")
    jd_text_input = st.text_area("Paste JD text here", height=200, placeholder="Paste the job description here...")
    uploaded_jd = st.file_uploader("Or upload JD (txt)", type=["txt"])

if uploaded_jd and not jd_text_input.strip():
    jd_text_input = uploaded_jd.read().decode("utf-8")

if st.button("Analyze Resume", type="primary"):

    if not uploaded_resume:
        st.error("⚠️ Please upload a resume file to analyze.")
        st.stop()

    with st.spinner("Analyzing resume..."):
        resume_text = extract_text_from_file(uploaded_resume)
        resume_text = clean_text(resume_text)
        if not resume_text.strip():
            st.error("❌ Unable to extract text from the resume. Please try a different file format.")
            st.stop()

        jd_text = jd_text_input.strip()
        if not jd_text:
            st.warning("⚠️ No job description provided. Analysis will be limited to general insights.")
            jd_text = ""

        # Top keywords from JD (if JD present)
        top_keywords = extract_top_keywords(jd_text, top_k=15) if jd_text else []

        # Skill match (Optimized)
        found_skills, missing_skills = match_skills(resume_text)

        # Semantic similarity
        if jd_text:
            sim = semantic_similarity(resume_text, jd_text)
            sim_percent = round(sim * 100, 1)
        else:
            sim = 0.0
            sim_percent = None

        # Keyword presence
        kw_rows = []
        for kw in top_keywords:
            # Use regex for whole word match
            present = bool(re.search(r"\b" + re.escape(kw) + r"\b", resume_text, flags=re.I))
            kw_rows.append({"Keyword": kw, "Found": "✅" if present else "❌"})

        # Recommendations
        recs = generate_recommendations(resume_text, jd_text, top_keywords, found_skills, missing_skills, sim)

    # ---------------- Results ----------------
    st.markdown("---")
    
    # 3-Column Summary
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="stCard">
            <p style="font-size: 1rem; color: #ccc; margin-bottom: 5px;">Total Words</p>
            <p class="metric-value">{len(resume_text.split())}</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="stCard">
            <p style="font-size: 1rem; color: #ccc; margin-bottom: 5px;">Skills Detected</p>
            <p class="metric-value">{len(found_skills)}</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        if sim_percent is not None:
            # Custom progress bar
            pb_width = f"{sim_percent}%"
            pb_color = "#FFD700" if sim_percent >= 70 else "#00BFFF" if sim_percent >= 50 else "#FF4500"
            st.markdown(f"""
            <div class="stCard">
                <p style="font-size: 1rem; color: #ccc; margin-bottom: 5px;">Visual Match</p>
                <p class="metric-value" style="color: {pb_color}">{sim_percent}%</p>
                <div style="background-color: rgba(255,255,255,0.2); border-radius: 5px; height: 10px; margin-top: 5px;">
                    <div style="background-color: {pb_color}; width: {pb_width}; height: 100%; border-radius: 5px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="stCard">
                <p style="font-size: 1rem; color: #ccc; margin-bottom: 5px;">Match Score</p>
                <p class="metric-value">N/A</p>
                <p style="font-size: 0.8rem; color: #999;">(No JD provided)</p>
            </div>
            """, unsafe_allow_html=True)

    # Detailed Analysis Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["💡 Recommendations", "🛠 Skills Analysis", "📊 Keywords", "📄 Resume Preview"])

    with tab1:
        st.subheader("Actionable Insights")
        if recs:
            for r in recs:
                st.info(f"**Tip:** {r}")
        else:
            st.success("🎉 Great job! Your resume looks well-optimized.")

    with tab2:
        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader(f"✅ Found Skills ({len(found_skills)})")
            if found_skills:
                st.write(", ".join(found_skills))
            else:
                st.write("No specific skills detected.")
        with col_b:
            st.subheader("⚠️ Missing Skills")
            if missing_skills:
                st.write(", ".join(missing_skills[:30]))
            else:
                st.write("Great coverage of common skills!")

    with tab3:
        st.subheader("Job Description Keywords")
        if top_keywords:
            st.dataframe(pd.DataFrame(kw_rows), use_container_width=True)
        else:
            st.write("Enter a Job Description to see keyword analysis.")

    with tab4:
        st.subheader("Extracted Text Review")
        st.text_area("Raw Text", resume_text, height=300)


# Footer with credits
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px 0; margin-top: 40px;">
    <p style="color: #666; font-size: 0.85rem; margin-bottom: 8px;">
        🚀 Built with ❤️ by <strong style="color: #FFD700;">NFS Programming</strong>
    </p>
    <p style="color: #555; font-size: 0.75rem;">
        © 2026 NFS Programming. All rights reserved. | 
        <a href="https://github.com/nfsprogramming/smartresumeanlyzer" target="_blank" style="color: #00BFFF; text-decoration: none;">View on GitHub</a>
    </p>
    <p style="color: #444; font-size: 0.7rem; margin-top: 8px;">
        Powered by Streamlit • Sentence Transformers • NLTK
    </p>
</div>
""", unsafe_allow_html=True)
