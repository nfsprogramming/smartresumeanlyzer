"""
Resume Version Control Page
"""

import streamlit as st
from database.db_manager import db_manager
from utils.ui import setup_page_styling

st.set_page_config(page_title="Resume Versions", page_icon="📝")
setup_page_styling()

st.title("📝 Resume Version Vault")
st.markdown("### Track, Compare, and Switch between resume versions.")

# Current Session Resume
if 'resume_text' in st.session_state and st.session_state.resume_text:
    st.subheader("Current Session Resume")
    with st.expander("View Current Text", expanded=False):
        st.text_area("Live Content", st.session_state.resume_text, height=200, disabled=True)
        
    c1, c2 = st.columns([2, 1])
    with c1:
        v_name = st.text_input("Name this version", placeholder="e.g. Master V1, Google Tailored")
    with c2:
        if st.button("💾 Save to Vault"):
            if v_name:
                db_manager.save_version(v_name, st.session_state.resume_text)
                st.success("Saved!")
                st.rerun()
            else:
                st.error("Please name this version.")
else:
    st.info("Upload a resume on Home to start tracking versions.")

st.divider()

# Vault List
st.subheader("📜 Version History")
df = db_manager.get_versions()

if not df.empty:
    for index, row in df.iterrows():
        with st.expander(f"📌 {row['version_name']} ({row['created_at']})"):
            st.text_area("Content", row['content'], height=150, key=f"v_{row['id']}")
            
            c_act1, c_act2, c_act3 = st.columns(3)
            with c_act1:
                if st.button("📂 Load / Rollback", key=f"load_{row['id']}"):
                    st.session_state.resume_text = row['content']
                    st.session_state.resume_name = row['version_name']
                    st.success(f"Loaded '{row['version_name']}' into active session!")
            
            with c_act2:
                st.download_button(
                    label="⬇️ Download TXT",
                    data=row['content'],
                    file_name=f"{row['version_name']}.txt",
                    mime="text/plain",
                    key=f"dl_{row['id']}"
                )
                
            with c_act3:
                if st.button("🗑️ Delete", key=f"del_{row['id']}"):
                    db_manager.delete_version(row['id'])
                    st.rerun()
else:
    st.info("Vault is empty. Save your first version above.")
