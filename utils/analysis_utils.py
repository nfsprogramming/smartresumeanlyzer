"""
Analysis utilities for Smart Resume Analyzer
Contains core logic for keywords, skills, and similarity
"""

import re
from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer, util
import streamlit as st
from config import ALL_SKILLS, Settings

# Load model once
@st.cache_resource
def load_sentence_transformer():
    return SentenceTransformer(Settings.SENTENCE_TRANSFORMER_MODEL)

EMBED_MODEL = load_sentence_transformer()

def extract_top_keywords(jd_text: str, top_k=10) -> List[str]:
    if not jd_text or not jd_text.strip():
        return []
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

def match_skills(resume_text: str, skills_list=ALL_SKILLS) -> Tuple[List[str], List[str]]:
    rt = resume_text.lower()
    found = []
    missing = []
    
    # Use config skills if not provided
    if not skills_list:
        skills_list = ALL_SKILLS
        
    for s in skills_list:
        if re.search(r"\b" + re.escape(s.lower()) + r"\b", rt):
            found.append(s)
        else:
            missing.append(s)
    return list(set(found)), list(set(missing)) # Ensure unique

def semantic_similarity(a: str, b: str) -> float:
    emb_a = EMBED_MODEL.encode(a, convert_to_tensor=True)
    emb_b = EMBED_MODEL.encode(b, convert_to_tensor=True)
    sim = util.cos_sim(emb_a, emb_b).item()
    return max(0.0, min(1.0, float(sim)))

def generate_recommendations(resume_text: str, jd_text: str, keywords: List[str], found_skills: List[str], missing_skills: List[str], sim_score: float) -> List[str]:
    recs = []
    # keyword suggestions
    missing_keywords = [k for k in keywords if not re.search(r"\b" + re.escape(k) + r"\b", resume_text, flags=re.I)]
    
    if missing_keywords:
        recs.append(f"Include these important keywords from the job description: {', '.join(missing_keywords[:5])}")
    
    # skills
    if missing_skills and jd_text:
        # Only suggest missing skills that are likely relevant (overlap with JD?)
        # For simplicity, we just take the top few from the missing list that might match JD keywords
        # But here we just show strict missing skills
        recs.append(f"Consider adding relevant skills: {', '.join(missing_skills[:5])}")
        
    # metrics
    if "0" not in resume_text and "percent" not in resume_text.lower():
        recs.append("Add quantifiable achievements (e.g., 'Improved performance by 20%').")
        
    if sim_score < 0.6:
        recs.append("Low match score. Tailor your resume summary and skills specifically to this JD.")
        
    return recs
