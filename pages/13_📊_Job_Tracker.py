"""
Job Application Tracker Module
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from database.db_manager import db_manager
from utils.ui import setup_page_styling, get_lottie
from streamlit_lottie import st_lottie

st.set_page_config(page_title="Job Tracker", page_icon="📊", layout="wide")
setup_page_styling()

c1, c2 = st.columns([1, 6])
with c1:
    lottie = get_lottie("rocket")
    if lottie:
        st_lottie(lottie, height=100)
    else:
        st.markdown("🚀")
with c2:
    st.title("Job Application Tracker")
    st.markdown("### Manage your applications and track success.")

# --- Notifications / Alerts ---
st.subheader("🔔 Alerts")
df = db_manager.get_applications()

alerts = []
if not df.empty:
    for index, row in df.iterrows():
        # Check if applied > 14 days ago and no update
        if row['status'] == 'Applied':
            try:
                # Basic date parsing
                applied_date = datetime.strptime(row['date_applied'], "%Y-%m-%d")
                if datetime.now() - applied_date > timedelta(days=14):
                    alerts.append(f"Follow up with **{row['company']}** ({row['role']}) - Applied 14+ days ago.")
            except:
                pass

if alerts:
    for a in alerts:
        st.warning(a)
else:
    st.success("✅ No pending follow-ups.")

st.divider()

# --- Add New Application ---
with st.expander("➕ Add New Application", expanded=False):
    c1, c2, c3 = st.columns(3)
    with c1:
        company = st.text_input("Company Name")
    with c2:
        role = st.text_input("Role Title")
    with c3:
        status = st.selectbox("Status", ["Applied", "Screening", "Interview", "Offer", "Rejected"])
        
    c4, c5 = st.columns(2)
    with c4:
        date = st.date_input("Date Applied", datetime.now())
    with c5:
        score = st.number_input("ATS Score (Optional)", 0, 100, 0)
        
    notes = st.text_area("Notes")
    
    if st.button("Save Application", type="primary"):
        if company and role:
            db_manager.add_application(company, role, status, str(date), score, notes)
            st.success("Tracked!")
            st.rerun()
        else:
            st.error("Company and Role are required.")

# --- View / Edit Applications ---
st.subheader("YOUR APPLICATIONS")

if not df.empty:
    # Editable Dataframe
    edited_df = st.data_editor(
        df,
        column_config={
            "status": st.column_config.SelectboxColumn(
                "Status",
                options=["Applied", "Screening", "Interview", "Offer", "Rejected"],
                required=True,
            ),
            "date_applied": st.column_config.DateColumn("Date"),
            "ats_score": st.column_config.ProgressColumn("Score", min_value=0, max_value=100)
        },
        disabled=["id"],
        hide_index=True,
        use_container_width=True,
        key="editor"
    )
    
    # Logic to handle updates is complex with data_editor in basic streamlit versions without session state tracking
    # Ideally we use callbacks, but for simplicity, we provide specific actions below.
    
    st.info("💡 To update status permanently or delete, use the controls below.")
    
    c_act1, c_act2 = st.columns([2, 1])
    with c_act1:
        app_to_edit = st.selectbox("Select Application to Update", df['company'] + " - " + df['role'])
        new_stat = st.selectbox("New Status", ["Applied", "Screening", "Interview", "Offer", "Rejected"], key="new_s")
        if st.button("Update Status"):
            # Find ID
            # This is a bit Hacky, relies on string match. Better to select by ID in real app.
            row = df[df['company'] + " - " + df['role'] == app_to_edit].iloc[0]
            db_manager.update_status(int(row['id']), new_stat)
            st.success("Updated!")
            st.rerun()
            
    with c_act2:
        st.write("Danger Zone")
        if st.button("Delete Selected App"):
             row = df[df['company'] + " - " + df['role'] == app_to_edit].iloc[0]
             db_manager.delete_application(int(row['id']))
             st.success("Deleted.")
             st.rerun()

else:
    st.info("No applications tracked yet.")
