"""
GitHub Portfolio Page
"""

import streamlit as st
import plotly.express as px
import pandas as pd
from modules.github_analyzer import github_analyzer
from utils.ui import setup_page_styling, get_lottie
from streamlit_lottie import st_lottie

st.set_page_config(page_title="GitHub Portfolio", page_icon="💻")
setup_page_styling()

c1, c2 = st.columns([1, 4])
with c1:
    lottie = get_lottie("coding")
    if lottie:
        st_lottie(lottie, height=100)
    else:
        st.markdown("💻")
with c2:
    st.title("GitHub Profile Analyzer")
    st.markdown("### Visualize your coding footprint and map it to your skills.")

# Input
username = st.text_input("Enter GitHub Username:", placeholder="e.g. nfsprogramming")

if st.button("Analyze Profile", type="primary"):
    if not username:
        st.warning("Please enter a username.")
    else:
        with st.spinner(f"Fetching data for @{username}..."):
            data = github_analyzer.analyze_profile(username)
            
            if data.get("error"):
                st.error(f"Error: {data['error']}")
            else:
                stats = data["stats"]
                langs = data["languages"]
                projects = data["top_projects"]
                
                # Header
                c1, c2 = st.columns([1, 4])
                with c1:
                    st.image(stats["avatar"], width=100)
                with c2:
                    st.markdown(f"## {stats['name']}")
                    st.markdown(f"_{stats['bio']}_")
                    st.markdown(f"🔗 [{stats['url']}]({stats['url']})")
                
                # Metrics
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Repositories", stats["repos"])
                m2.metric("Followers", stats["followers"])
                m3.metric("Years Active", f"{2026 - stats['created_at']}+") # 2026 is current year
                m4.metric("Top Language", list(langs.keys())[0] if langs else "N/A")
                
                st.divider()
                
                # Charts & Projects
                col_chart, col_proj = st.columns([1, 1])
                
                with col_chart:
                    st.subheader("🛠 Technical Base")
                    if langs:
                        # Pie chart
                        df_lang = pd.DataFrame(list(langs.items()), columns=['Language', 'Percentage'])
                        fig = px.pie(df_lang, values='Percentage', names='Language', hole=0.4)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No language data found.")
                        
                    st.subheader("🏷️ Top Topics")
                    topics = data["topics"]
                    if topics:
                        st.write(", ".join([f"`{t[0]}`" for t in topics]))
                
                with col_proj:
                    st.subheader("🏆 Top Projects")
                    for p in projects:
                        with st.expander(f"⭐ {p['stars']}: {p['name']}", expanded=True):
                            st.write(p['desc'])
                            st.markdown(f"**Language:** {p['language']}")
                            st.markdown(f"[View Repo]({p['url']})")
