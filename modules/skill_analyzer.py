"""
Skill Confidence Estimator Module
Estimates skill proficiency (Beginner/Intermediate/Advanced) based on resume context
"""

import re
from typing import Dict, List, Tuple
from config import Settings

class SkillAnalyzer:
    """
    Analyzes skills and estimates confidence levels.
    """
    
    def __init__(self):
        self.years_pattern = re.compile(r'(\d+)\+?\s*years?', re.IGNORECASE)
        
    def analyze_proficiency(self, resume_text: str, found_skills: List[str]) -> Dict[str, str]:
        """
        Estimate proficiency for each found skill.
        Returns a dict: {'skill': 'Advanced', ...}
        """
        proficiency_map = {}
        
        # Pre-process text for better searching
        text_lower = resume_text.lower()
        
        for skill in found_skills:
            level = self._estimate_single_skill(text_lower, skill)
            proficiency_map[skill] = level
            
        return proficiency_map

    def _estimate_single_skill(self, text: str, skill: str) -> str:
        """
        Estimate level for a single skill based on heuristics.
        """
        skill_lower = skill.lower()
        
        # 1. Check for explicit level mentions
        # e.g., "Advanced knowledge of Python", "Intermediate Java"
        expert_keywords = ["advanced", "expert", "proficient", "strong", "senior", "lead", "architect"]
        intermediate_keywords = ["intermediate", "experience with", "familiar"]
        beginner_keywords = ["beginner", "basic", "knowledge of", "exposure to", "junior"]
        
        # Search window: look at words around the skill
        # This is a simple regex lookahead/behind approximation
        
        # Check context sentences containing the skill
        sentences = [s.strip() for s in text.split('.') if skill_lower in s]
        full_context = " ".join(sentences)
        
        score = 0
        
        # Heuristic 1: Keywords
        for kw in expert_keywords:
            if kw in full_context:
                score += 3
        for kw in intermediate_keywords:
            if kw in full_context:
                score += 2
        
        # Heuristic 2: Frequency
        # If a skill is mentioned many times, it's likely a core strength
        count = text.count(skill_lower)
        if count > 5:
            score += 2
        elif count > 2:
            score += 1
            
        # Heuristic 3: Years of Experience (very rough association)
        # Look for "X years" near the skill
        # This is hard to attribute correctly without deep NLP, but we try specific patterns
        # e.g., "5 years of Python"
        years_match = re.search(fr'(\d+)\+?\s*years?.*{re.escape(skill_lower)}', text)
        if not years_match:
            # Try reverse: "Python (5 years)"
            years_match = re.search(fr'{re.escape(skill_lower)}.*?(\d+)\+?\s*years?', text)
            
        if years_match:
            try:
                years = int(years_match.group(1))
                if years >= Settings.SKILL_ADVANCED_THRESHOLD:
                    return "Advanced"
                elif years >= Settings.SKILL_INTERMEDIATE_THRESHOLD:
                    return "Intermediate"
                else:
                    return "Beginner"
            except:
                pass

        # Final Classification
        if score >= 4:
            return "Advanced"
        elif score >= 2:
            return "Intermediate"
        else:
            return "Beginner"

    def calculate_skill_gap(self, found_skills: List[str], jd_keywords: List[str]) -> List[str]:
        """
        Identify critical missing skills from JD keywords.
        """
        missing = []
        found_set = {s.lower() for s in found_skills}
        
        for kw in jd_keywords:
            kw_clean = kw.lower()
            if kw_clean not in found_set:
                # Basic check: is the keyword actually a known skill?
                # For now, we assume high-value keywords from JD often represent skills
                missing.append(kw)
                
        return missing

skill_analyzer = SkillAnalyzer()
