# 📘 Smart Resume Analyzer 2.0 - User Manual

## 👋 Welcome
Congratulations on deploying the Smart Resume Analyzer 2.0! This Enterprise-Grade AI platform is designed to optimize every stage of your job search.

---

## 🚀 Quick Start
1.  **Launch the App**: Run `start_app.bat` (Windows) or `streamlit run app.py`.
2.  **Upload Resume**: Go to **Home** and upload your PDF/DOCX resume. This "Master Resume" will be used across all other tools.

---

## 🛠️ Feature Guide

### 1. 📊 Resume Analysis
*   **What it does**: Breaks down your resume into key metrics (Word Count, Action Verbs, Skills).
*   **How to use**: View the dashboard immediately after upload. Look at the "Skill DNA" to see your proficiency levels.

### 2. 🔍 JD Fetcher
*   **What it does**: Extracts job descriptions from generic URLS (e.g. LinkedIn, Indeed).
*   **How to use**: Paste a URL and click "Fetch". If successful, click **"Use this JD for Analysis"** to save it for comparison.

### 3. ✍️ Resume Optimizer
*   **What it does**: Rewrites your resume sections to match a specific JD or Role.
*   **How to use**: 
    1. Select a section (e.g., "Summary" or "Work Experience").
    2. Enter the target role.
    3. Click "Optimize". Copy the AI-generated text back to your document.

### 4. 💡 Project Recommendations
*   **What it does**: Suggests portfolio projects based on skills you are *missing*.
*   **How to use**: The tool automatically detects gaps. Browse the cards for project ideas (Beginner to Advanced).

### 5. 📚 Learning Path
*   **What it does**: Generates a curriculum to learn missing skills.
*   **How to use**: Select skills to learn and click "Generate Roadmap". It provides links to free resources.

### 6. 🎯 Interview Prep & Mock Interview
*   **Prep**: Generates a list of questions (Technical & Behavioral) for your target role.
*   **Mock Interview**: Chat with an AI bot that acts as a hiring manager. It remembers your previous answers!

### 7. 🧠 Resume Intelligence
*   **Authenticity Check**: Flags buzzwords ("Ninja", "Rockstar") that recruiters hate.
*   **Bias Check**: Ensures your language is inclusive and professional.
*   **Heatmap**: visualizes where your resume is strongest.

### 8. 🏢 ATS Simulator
*   **What it does**: Simulates how **Google, Amazon, or Apple** algorithms would score your resume.
*   **How to use**: Select a company. The tool checks for specific cultural keywords (e.g. Amazon's "Customer Obsession").

### 9. 📊 Job Tracker
*   **What it does**: A CRM for your job search.
*   **Features**:
    *   **Add**: Log every application.
    *   **Alerts**: The top of the page warns you if an app is 14+ days old with no status update.
    *   **Edit**: Update status to "Interviewing" or "Offer".

### 10. 📝 Resume Vault
*   **What it does**: Version control for your resume.
*   **How to use**:
    *   **Save**: After editing or uploading, click "Save to Vault" and name it (e.g. "Google Resume").
    *   **Rollback**: Load any old version instantly to be the active resume.

---

## ⚙️ Settings & Admin
*   **API Keys**: Enter your OpenAI Key here if you didn't set it in `.env`.
*   **Clear Data**: Use "Wipe Database" to reset the Job Tracker completely.

---

## ❓ FAQ

**Q: Why does the AI say "OpenAI Key Missing"?**
A: You need to put your API Key in `.env` or the Settings page. Without it, the app runs in "Local/Demo" mode with limited capability.

## 🌐 Cloud Deployment (Render.com)
The project is optimized for deployment on **Render.com** using the included `Dockerfile` and `render.yaml` blueprint.

### 🚀 One-Click Deployment
1.  **Fork/Push your repo to GitHub**.
2.  **Log in to Render.com**.
3.  **Go to "Blueprints"** and connect your repository. 
4.  Render will automatically detect the `render.yaml` and set up:
    *   **The Web Service** (Docker-based).
    *   **Persistent Storage** (to save your Job Tracker data between restarts).
5.  **Environment Variables**: You will be prompted to enter your `OPENAI_API_KEY`, `GITHUB_TOKEN`, and `YOUTUBE_API_KEY`.

### ⚠️ Performance Tip
Since this app uses large AI models (**Torch**, **SentenceTransformers**), I recommend the **"Starter" ($7/mo)** plan on Render. The **Free Tier (512MB RAM)** will likely experience "Out of Memory" crashes when loading the NLP modules.
