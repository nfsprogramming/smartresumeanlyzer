"""
LinkedIn Sync Page
Compare profile with resume
"""

import streamlit as st
import pdfplumber
import io
from utils.ui import setup_page_styling

st.set_page_config(page_title="LinkedIn Sync", page_icon="🔗")
setup_page_styling()

st.title("🔗 LinkedIn Profile Sync")
st.markdown("### Align your Resume and LinkedIn Profile.")

col1, col2 = st.columns([2, 1])

with col1:
    st.info("""
    **Instruction:**
    1. Go to your LinkedIn Profile.
    2. Click 'More' -> 'Save to PDF'.
    3. Upload that PDF here.
    """)
    uploaded_li = st.file_uploader("Upload LinkedIn PDF", type=["pdf"])

with col2:
    st.markdown("### Why Sync?")
    st.markdown("""
    Recruiters look for consistency.
    - Dates match?
    - Job titles match?
    - Skills match?
    """)

if uploaded_li and 'resume_text' in st.session_state and st.session_state.resume_text:
    # Basic comparison logic
    with st.spinner("Analyzing consistency..."):
        # Extract text from LinkedIn PDF
        li_text = ""
        try:
            with pdfplumber.open(uploaded_li) as pdf:
                for page in pdf.pages:
                    li_text += page.extract_text() + "\n"
        except Exception:
            st.error("Error parsing LinkedIn PDF.")
            
        if li_text:
            st.success("LinkedIn Profile Parsed!")
            
            # Simple check: Word Overlap (Jaccard)
            res_words = set(st.session_state.resume_text.lower().split())
            li_words = set(li_text.lower().split())
            
            common = res_words.intersection(li_words)
            overlap = len(common) / len(res_words) * 100
            
            st.metric("Consistency Score", f"{int(overlap)}%")
            
            st.subheader("Discrepancies found:")
            # Find big discrepancies (e.g. Resume has "Manager" but LinkedIn doesn't?)
            # This is hard to do perfectly with raw text, so we do general advice.
            
            if overlap < 40:
                st.warning("⚠️ Low overlap. Your resume and LinkedIn seem to tell different stories.")
            elif overlap > 80:
                st.success("✅ High consistency.")
            else:
                st.info("ℹ️ Moderate consistency. Ensure job dates align perfectly.")
                
            st.markdown("### Missing from LinkedIn?")
            # Words in resume but not in LinkedIn (filtering common stopwords)
            unique_resume = list(res_words - li_words)
            # Filter short words
            unique_resume = [w for w in unique_resume if len(w) > 5]
            st.write(", ".join(unique_resume[:20]))
