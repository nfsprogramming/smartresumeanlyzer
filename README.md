# Smart Resume Analyzer

An AI-powered resume analysis tool that helps optimize resumes for Applicant Tracking Systems (ATS) with intelligent insights and recommendations.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-green.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.39+-red.svg)

## 🚀 Features

- **📄 Resume Parsing**: Supports PDF, DOCX, and TXT formats with robust text extraction
- **🤖 AI-Powered Analysis**: Uses Sentence-Transformers for semantic similarity matching
- **🎯 Skill Matching**: Optimized algorithm to identify technical and soft skills
- **🔍 Keyword Extraction**: TF-IDF based keyword extraction from job descriptions
- **💡 Smart Recommendations**: Actionable insights to improve resume quality
- **📊 Interactive Dashboard**: Modern, dark-themed interface with tabs and visualizations
- **⚡ Fast Performance**: Cached models for quick analysis

## 🎨 Premium UI

- Modern dark theme with gold accents
- Glassmorphism design elements
- Interactive tabs and visualizations
- Responsive layout
- Smooth animations

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **AI/ML**: Sentence-Transformers, NLTK, scikit-learn
- **Data Processing**: Pandas, NumPy
- **Document Parsing**: pdfplumber, docx2txt
- **Deep Learning**: PyTorch

## 📦 Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/nfsprogramming/smartresumeanlyzer.git
   cd smartresumeanlyzer
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

The app will open in your default browser at `http://localhost:8501`.

## 🌐 Cloud Deployment

Deploy to Streamlit Cloud for free:

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click "New app" and select your repository
5. Set main file: `app.py`
6. Click "Deploy"

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## 📖 Usage

1. **Upload Resume**: Upload your resume in PDF, DOCX, or TXT format
2. **Add Job Description**: Paste or upload the job description
3. **Analyze**: Click "Analyze Resume" to get insights
4. **Review Results**: 
   - View match score and statistics
   - Check skill analysis
   - Review keyword matching
   - Read actionable recommendations

## 🎯 How It Works

1. **Text Extraction**: Extracts text from uploaded resume
2. **Preprocessing**: Cleans and normalizes text
3. **Keyword Analysis**: Uses TF-IDF to extract important keywords from JD
4. **Skill Matching**: Identifies technical and soft skills
5. **Semantic Analysis**: Calculates similarity between resume and JD using AI
6. **Recommendations**: Generates personalized improvement suggestions

## 📊 Analysis Features

- **Match Score**: AI-powered semantic similarity percentage
- **Skill Detection**: Identifies 50+ common technical and soft skills
- **Keyword Matching**: Shows which JD keywords are present/missing
- **Action Verb Count**: Analyzes use of strong action verbs
- **Quantifiable Metrics**: Suggests adding measurable achievements

## 🔧 Configuration

The app includes pre-configured settings in `.streamlit/config.toml`:
- Dark theme
- Gold primary color
- Monospace font
- Custom styling

## 📝 Notes

- **First Run**: NLTK data and AI models download automatically on first run
- **Performance**: Sentence transformer model (~90MB) is cached after first download
- **Privacy**: All processing happens locally or on your Streamlit Cloud instance

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Developer

**NFS Programming**
- GitHub: [@nfsprogramming](https://github.com/nfsprogramming)
- Repository: [smartresumeanlyzer](https://github.com/nfsprogramming/smartresumeanlyzer)

## 🙏 Acknowledgments

- Streamlit for the amazing framework
- Sentence-Transformers for semantic analysis
- NLTK for natural language processing
- The open-source community

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review deployment guide

---

**Built with ❤️ by NFS Programming** | © 2026 All Rights Reserved
