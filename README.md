# 🚀 Smart Resume Analyzer 2.0

An Enterprise-Grade AI Career Platform that helps you land your dream job using advanced Job Description analysis, Resume Rewriting, and Mock Interviews.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B.svg)
![OpenAI](https://img.shields.io/badge/AI-OpenAI%20%7C%20Gemini-green)

## 🌟 Features

This application includes **18+ Advanced Tools** organized into a modular dashboard:

### 🧠 Core Analysis
*   **Resume Analysis**: Deep insights into keywords, structure, and action verbs.
*   **JD Auto-Fetcher**: Scrape job descriptions directly from LinkedIn/Indeed URLs.
*   **Skill Gap Analysis**: Identify missing critical skills for any job.
*   **Resume Optimizer**: AI-powered rewriting of your summary and bullet points.

### 🎓 Learning & Prep
*   **Learning Path**: Auto-generated course roadmap (YouTube/Coursera) for missing skills.
*   **Interview Prep**: Generates role-specific technical & behavioral questions.
*   **Mock Interview Bot**: Real-time chat simulation with an AI hiring manager.
*   **Project Recommender**: Suggests portfolio projects to fill skill gaps.

### 💼 Platform Integrations
*   **GitHub Portfolio**: Analyzes your GitHub profile to showcase your coding stats.
*   **LinkedIn Sync**: Compares your resume against your LinkedIn PDF export.
*   **Student Coach**: Specialized mode for freshers/interns focusing on potential over experience.

### ⚙️ advanced Tools
*   **ATS Emulator**: Simulates screening algorithms of Google, Amazon, and Apple.
*   **Bias Checker**: Detects unconscious bias (gender/age) in your writing.
*   **Job Tracker**: Database-backed application tracking with auto-alerts.
*   **Resume Vault**: Version control system to save and rollback resume versions.

---

## 🛠️ Installation

1.  **Clone the repository** (if not already downloaded).
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Setup Environment Variables**:
    *   Rename `.env.example` to `.env`.
    *   Add your API Keys (OpenAI is recommended for full features).
    ```ini
    OPENAI_API_KEY=sk-...
    GITHUB_TOKEN=ghp_... (Optional)
    YOUTUBE_API_KEY=... (Optional)
    ```

## 🚀 Usage

Run the dashboard locally:

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

## 📂 Project Structure

*   `app.py`: Main Dashboard and entry point.
*   `pages/`: Individual tools (JD Fetcher, Rewriter, etc.).
*   `modules/`: Core logic (AI engines, Analyzers).
*   `utils/`: Helper functions and UI Design System.
*   `database/`: SQLite database for the Job Tracker.

## 🎨 UI & Design

The app features a **Premium Glassmorphism Design System** (`utils/ui.py`) with:
*   Animated Deep Space Backgrounds.
*   Lottie Animations.
*   Dark Mode suited for long coding sessions.

---
**Author**: NFS Photographer
**Version**: 2.0
