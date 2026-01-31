"""
UI Design System for Smart Resume Analyzer
Centralizes styling, animations, and reusable components.
"""

import streamlit as st
import requests

# --- Animated Assets ---
LOTTIE_AI_ANALYSIS = "https://lottie.host/80e98033-1748-4e89-9818-62d355024446/q8z7D7q8D4.json" # Robot Scanning
LOTTIE_CODING = "https://lottie.host/92a18854-e659-4673-8a9d-541240212009/1Xz2j3j21Z.json" # Coding Screen
LOTTIE_INTERVIEW = "https://lottie.host/96b46481-9969-450f-902c-420108930432/m6tq1T3T12.json" # Interview Chat
LOTTIE_ROCKET = "https://lottie.host/31804139-335c-4340-8438-685718a70903/Z8T12T1T88.json" # Rocket Launch3

@st.cache_data(ttl=3600) # Cache for 1 hour -> Huge Speed Boost
def load_lottie_url(url: str):
    try:
        r = requests.get(url, timeout=2)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

def setup_page_styling():
    """
    Injects global CSS for the premium feel.
    """
    st.markdown("""
        <style>
        /* Import Font: Roboto */
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
        
        /* Logo Glow Effect */
        [data-testid="stImage"] img, [data-testid="stLottie"] {
            filter: drop-shadow(0 0 10px rgba(0, 191, 255, 0.5));
            transition: filter 0.3s ease;
        }
        [data-testid="stImage"] img:hover, [data-testid="stLottie"]:hover {
            filter: drop-shadow(0 0 20px rgba(0, 191, 255, 0.8));
        }
        
        /* --- 1. KEYFRAMES --- */
        @keyframes moveStars { from { background-position: 0 0; } to { background-position: 1000px 1000px; } }
        @keyframes float { 0% { transform: translateY(0px); } 50% { transform: translateY(-6px); } 100% { transform: translateY(0px); } }
        @keyframes fadeInUp { from { opacity: 0; transform: translate3d(0, 30px, 0); } to { opacity: 1; transform: translate3d(0, 0, 0); } }
        @keyframes pulseGlow { 0% { box-shadow: 0 0 5px rgba(0,191,255,0.2); } 50% { box-shadow: 0 0 20px rgba(0,191,255,0.6); } 100% { box-shadow: 0 0 5px rgba(0,191,255,0.2); } }

        /* --- 2. GLOBAL RESET --- */
        html, body, [class*="css"], [data-testid="stSidebar"], button, input, textarea {
            font-family: 'Roboto', sans-serif !important;
            color: #E0E0E0 !important;
        }

        /* --- 3. CLEAN BACKGROUND (No Animation) --- */
        .stApp {
            background: #050505;
            background: radial-gradient(circle at center, #1a1a2e 0%, #000000 100%);
            color: #d0d0d0;
        }

        /* --- 4. GLASS CARDS with 3D HOVER --- */
        .glass-container {
            background: rgba(22, 22, 28, 0.75);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            padding: 28px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            margin-bottom: 25px;
            
            /* Animation */
            animation: fadeInUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); /* Spring transition */
        }
        
        .glass-container:hover {
            transform: translateY(-8px) scale(1.02);
            background: rgba(26, 26, 35, 0.85);
            border: 1px solid rgba(0, 191, 255, 0.3);
            box-shadow: 0 20px 40px rgba(0, 191, 255, 0.15), 0 0 0 1px rgba(0, 191, 255, 0.2);
        }

        /* --- 5. NEON BUTTONS --- */
        .stButton>button {
            background: linear-gradient(135deg, #2b5876 0%, #4e4376 100%);
            border: none;
            border-radius: 12px;
            color: white !important;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            padding: 16px 24px;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }
        
        .stButton>button:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(78, 67, 118, 0.6);
            filter: brightness(1.2);
        }
        
        .stButton>button:active {
            transform: scale(0.98);
        }

        /* --- 6. INPUT FLOATING --- */
        .stTextInput > div > div > input, .stTextArea > div > div > textarea {
            background: rgba(255,255,255,0.03) !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            border-radius: 10px;
            color: white !important;
            transition: all 0.3s ease;
        }
        
        .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
            background: rgba(0,0,0,0.4) !important;
            border-color: #00BFFF !important;
            box-shadow: 0 0 15px rgba(0, 191, 255, 0.2);
            transform: translateY(-2px);
        }

        /* --- 7. SCROLLBAR --- */
        ::-webkit-scrollbar { width: 10px; }
        ::-webkit-scrollbar-track { background: #050505; }
        ::-webkit-scrollbar-thumb { background: linear-gradient(180deg, #2b5876, #4e4376); border-radius: 5px; }
        ::-webkit-scrollbar-thumb:hover { background: #00BFFF; }

        /* --- 8. HEADINGS --- */
        h1 {
            background: linear-gradient(120deg, #fff 0%, #00BFFF 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: float 6s ease-in-out infinite;
        }

        /* --- 9. SIDEBAR --- */
        [data-testid="stSidebar"] {
            background: rgba(10, 10, 15, 0.95);
            backdrop-filter: blur(10px);
            border-right: 1px solid rgba(255,255,255,0.05);
        }
        
        /* Fix tags */
        span[data-baseweb="tag"] { background: rgba(0,191,255,0.2) !important; border: 1px solid #00BFFF !important; }

        </style>
    """, unsafe_allow_html=True)

def get_lottie(type="ai"):
    """Get animation by type."""
    url = LOTTIE_AI_ANALYSIS
    if type == "coding": url = LOTTIE_CODING
    elif type == "interview": url = LOTTIE_INTERVIEW
    elif type == "rocket": url = LOTTIE_ROCKET
    
    # Try loading
    data = load_lottie_url(url)
    if data:
        return data
    # Fallback: Return None (Caller must handle) or a simple retry logic
    return None

def card(content, height=None):
    return f"""
    <div class="glass-container" style="{'height:'+str(height)+'px' if height else ''}">
        {content}
    </div>
    """

def colored_header(label, color="#00BFFF"):
    st.markdown(f"""
    <h3 style="color: {color}; border-bottom: 2px solid {color}; padding-bottom: 5px; margin-bottom: 20px;">
        {label}
    </h3>
    """, unsafe_allow_html=True)

# Backward Compatibility
def get_ai_animation():
    return get_lottie("ai")
