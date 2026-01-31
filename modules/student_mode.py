"""
Student Mode Module
Specialized logic for freshers and students
"""

import re

class StudentCoach:
    """
    Analyzes resume with a student/fresher lens.
    """
    
    def analyze_fresher_potential(self, text: str) -> dict:
        """
        Audit specifically for student strengths.
        """
        text_lower = text.lower()
        feedback = []
        score = 0
        
        # 1. Experience vs Projects Check
        has_internship = "intern" in text_lower or "trainee" in text_lower
        has_projects = "project" in text_lower
        
        if has_internship:
            feedback.append("✅ Internship detected. Excellent! Highlight specific outcomes.")
            score += 30
        else:
            feedback.append("⚠️ No internship keywords found. Focus heavily on academic projects.")
            
        if has_projects:
            score += 20
        else:
            feedback.append("❌ 'Projects' section weak or missing. This is critical for freshers.")
            
        # 2. Education Detail
        if "gpa" in text_lower or "cgpa" in text_lower:
            feedback.append("✅ GPA/CGPA included.")
            score += 10
        elif "cum laude" in text_lower or "honor" in text_lower:
            score += 10
        else:
            feedback.append("💡 Consider adding GPA (if > 3.0) or academic honors.")
            
        # 3. Certifications
        if "certification" in text_lower or "certificate" in text_lower:
            score += 15
            feedback.append("✅ Certifications section found.")
        else:
            feedback.append("💡 Add a Certifications section to validate technical skills.")
            
        # 4. Leadership (Clubs/Societies)
        clubs = ["club", "society", "volunteer", "hackathon", "committee", "president", "member"]
        if any(c in text_lower for c in clubs):
            score += 25
            feedback.append("✅ Active campus involvement detected (Clubs/Hackathons).")
        else:
            feedback.append("💡 Campus leadership/volunteering is a great soft-skill indicator for students.")
            
        return {
            "score": score,
            "feedback": feedback,
            "verdict": "Campus Hero" if score > 80 else "Strong Fresher" if score > 50 else "Needs More Portfolio"
        }

student_coach = StudentCoach()
