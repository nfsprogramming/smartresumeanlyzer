"""
Configuration file for Smart Resume Analyzer
Manages API keys, settings, and constants
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ============= API Keys =============
class APIKeys:
    # AI Models
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    
    # Job Boards
    LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID", "")
    LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET", "")
    INDEED_API_KEY = os.getenv("INDEED_API_KEY", "")
    
    # Learning Platforms
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
    COURSERA_API_KEY = os.getenv("COURSERA_API_KEY", "")
    UDEMY_API_KEY = os.getenv("UDEMY_API_KEY", "")
    
    # Social Platforms
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
    LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN", "")
    
    # Notifications
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_EMAIL = os.getenv("SMTP_EMAIL", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")

# ============= App Settings =============
class Settings:
    APP_NAME = "Smart Resume Analyzer"
    VERSION = "2.0.0"
    AUTHOR = "NFS Programming"
    GITHUB_REPO = "https://github.com/nfsprogramming/smartresumeanlyzer"
    
    # Database
    DB_PATH = "database/resume_analyzer.db"
    
    # File Upload Limits
    MAX_FILE_SIZE_MB = 10
    ALLOWED_RESUME_FORMATS = ["pdf", "docx", "doc", "txt"]
    ALLOWED_JD_FORMATS = ["txt", "pdf"]
    
    # AI Model Settings
    SENTENCE_TRANSFORMER_MODEL = "all-MiniLM-L6-v2"
    SPACY_MODEL = "en_core_web_sm"
    
    # Feature Flags
    ENABLE_MOCK_DATA = True  # Use mock data when APIs not available
    ENABLE_CACHING = True
    
    # Skill Confidence Thresholds
    SKILL_BEGINNER_THRESHOLD = 1  # years
    SKILL_INTERMEDIATE_THRESHOLD = 2
    SKILL_ADVANCED_THRESHOLD = 4
    
    # ATS Score Thresholds
    ATS_EXCELLENT = 80
    ATS_GOOD = 60
    ATS_FAIR = 40

# ============= Common Skills Database =============
TECHNICAL_SKILLS = {
    "Programming Languages": [
        "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust",
        "ruby", "php", "swift", "kotlin", "scala", "r", "matlab", "sql"
    ],
    "Web Development": [
        "react", "angular", "vue.js", "node.js", "express", "django", "flask",
        "fastapi", "spring boot", "asp.net", "html", "css", "sass", "tailwind",
        "bootstrap", "next.js", "nuxt.js", "svelte"
    ],
    "Mobile Development": [
        "react native", "flutter", "android", "ios", "swift", "kotlin",
        "xamarin", "ionic", "cordova"
    ],
    "Data Science & ML": [
        "machine learning", "deep learning", "nlp", "computer vision",
        "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy",
        "matplotlib", "seaborn", "plotly", "jupyter", "data analysis",
        "statistical modeling", "neural networks", "transformers"
    ],
    "Cloud & DevOps": [
        "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "gitlab ci",
        "github actions", "terraform", "ansible", "ci/cd", "devops",
        "microservices", "serverless", "lambda"
    ],
    "Databases": [
        "sql", "nosql", "mongodb", "postgresql", "mysql", "redis", "cassandra",
        "dynamodb", "elasticsearch", "oracle", "sql server", "sqlite"
    ],
    "Tools & Frameworks": [
        "git", "linux", "bash", "rest api", "graphql", "websockets",
        "oauth", "jwt", "agile", "scrum", "jira", "confluence"
    ]
}

SOFT_SKILLS = [
    "leadership", "communication", "teamwork", "problem solving",
    "critical thinking", "time management", "adaptability", "creativity",
    "collaboration", "project management", "analytical skills",
    "attention to detail", "decision making", "conflict resolution",
    "emotional intelligence", "mentoring", "presentation skills"
]

# Flatten technical skills for easy access
ALL_TECHNICAL_SKILLS = []
for category, skills in TECHNICAL_SKILLS.items():
    ALL_TECHNICAL_SKILLS.extend(skills)

ALL_SKILLS = ALL_TECHNICAL_SKILLS + SOFT_SKILLS

# ============= Action Verbs for Resume =============
ACTION_VERBS = [
    "achieved", "improved", "developed", "designed", "implemented",
    "created", "led", "managed", "optimized", "increased", "reduced",
    "launched", "built", "established", "streamlined", "automated",
    "collaborated", "coordinated", "delivered", "executed", "facilitated",
    "initiated", "pioneered", "spearheaded", "transformed", "accelerated"
]

# ============= Company ATS Keywords =============
COMPANY_ATS_KEYWORDS = {
    "Google": ["scalability", "distributed systems", "algorithms", "data structures",
               "system design", "innovation", "impact", "collaboration"],
    "Amazon": ["customer obsession", "ownership", "bias for action", "deliver results",
               "leadership principles", "scalable", "metrics-driven"],
    "Microsoft": ["growth mindset", "customer focus", "diversity", "inclusion",
                  "innovation", "cloud", "azure", "collaboration"],
    "Meta": ["impact", "move fast", "bold", "focus on long term", "build social value",
             "be open", "react", "scalability"],
    "Apple": ["innovation", "excellence", "attention to detail", "user experience",
              "design", "quality", "privacy", "security"],
    "Netflix": ["freedom and responsibility", "context not control", "highly aligned",
                "loosely coupled", "impact", "innovation"],
}

# ============= Project Ideas Database =============
PROJECT_IDEAS = {
    "Web Development": [
        {
            "name": "E-Commerce Platform",
            "skills": ["react", "node.js", "mongodb", "stripe api", "jwt"],
            "difficulty": "Intermediate",
            "description": "Full-stack e-commerce with payment integration"
        },
        {
            "name": "Social Media Dashboard",
            "skills": ["vue.js", "express", "postgresql", "websockets"],
            "difficulty": "Advanced",
            "description": "Real-time social media analytics dashboard"
        }
    ],
    "Data Science": [
        {
            "name": "Sentiment Analysis Tool",
            "skills": ["python", "nlp", "transformers", "streamlit"],
            "difficulty": "Intermediate",
            "description": "Analyze sentiment from social media posts"
        },
        {
            "name": "Recommendation System",
            "skills": ["python", "machine learning", "collaborative filtering", "flask"],
            "difficulty": "Advanced",
            "description": "Build a movie/product recommendation engine"
        }
    ],
    "Mobile Development": [
        {
            "name": "Fitness Tracker App",
            "skills": ["flutter", "firebase", "rest api", "charts"],
            "difficulty": "Intermediate",
            "description": "Track workouts and nutrition with analytics"
        },
        {
            "name": "Chat Application",
            "skills": ["react native", "websockets", "node.js", "mongodb"],
            "difficulty": "Advanced",
            "description": "Real-time messaging with media sharing"
        }
    ],
    "DevOps": [
        {
            "name": "CI/CD Pipeline",
            "skills": ["docker", "kubernetes", "jenkins", "terraform"],
            "difficulty": "Advanced",
            "description": "Automated deployment pipeline for microservices"
        }
    ]
}

# ============= Learning Resources =============
FREE_LEARNING_PLATFORMS = [
    "YouTube",
    "freeCodeCamp",
    "Coursera (Audit)",
    "edX (Audit)",
    "MIT OpenCourseWare",
    "Khan Academy",
    "W3Schools",
    "MDN Web Docs",
    "Official Documentation"
]
