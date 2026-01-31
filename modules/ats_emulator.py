"""
ATS Emulator Module
Simulates company-specific ATS systems (Google, Amazon, etc.)
"""

import re
from config import COMPANY_ATS_KEYWORDS

class ATSEmulator:
    """
    Simulates screening algorithms of major tech companies.
    """
    
    def simulate_scan(self, resume_text: str, company: str) -> dict:
        """
        Scan resume against company specific criteria.
        """
        text_lower = resume_text.lower()
        
        # 1. Keyword Match
        keywords = COMPANY_ATS_KEYWORDS.get(company, [])
        found_kws = []
        missing_kws = []
        
        for kw in keywords:
            if kw.lower() in text_lower:
                found_kws.append(kw)
            else:
                missing_kws.append(kw)
                
        # 2. Structure/Length Check (Generic Enterprise Standard)
        word_count = len(text_lower.split())
        length_status = "Good"
        if word_count < 400: length_status = "Too Short"
        if word_count > 1200: length_status = "Too Long"
        
        # 3. Specific Heuristics per Company
        company_feedback = []
        score = 0
        
        # Base score from keywords
        kw_score = (len(found_kws) / len(keywords) * 50) if keywords else 50
        score += kw_score
        
        if company == "Amazon":
            # Amazon loves "Leadership Principles"
            lps = ["customer obsession", "ownership", "invent and simplify", "learn and be curious", "deliver results"]
            lp_count = sum(1 for lp in lps if lp in text_lower)
            if lp_count >= 2:
                score += 20
                company_feedback.append("✅ Leadership Principles detected.")
            else:
                company_feedback.append("⚠️ Amazon heavily weighs Leadership Principles. explicitly mention outcomes that map to them.")
                
        elif company == "Google":
            # Google loves "Scale" and "Data"
            if "scale" in text_lower or "distributed" in text_lower or "petabyte" in text_lower:
                score += 20
                company_feedback.append("✅ Experience with scale detected.")
            else:
                company_feedback.append("⚠️ Google looks for 'scalability' and complexity. Highlight system design work.")
                
            if "gpa" in text_lower and re.search(r"[3-4]\.\d", text_lower):
                score += 5 # They historically cared, less now but still good
                
        elif company == "Apple":
            if "design" in text_lower or "user experience" in text_lower or "quality" in text_lower:
                score += 20
                company_feedback.append("✅ Focus on Product Quality/UX detected.")
            else:
                company_feedback.append("⚠️ Apple values 'Obsession with Detail' and 'UX'. Highlight your product sense.")
        
        # Formatting/General Check
        if score > 80:
            status = "likely_to_pass"
        elif score > 50:
            status = "manual_review"
        else:
            status = "auto_reject"
            
        return {
            "company": company,
            "score": min(100, int(score)),
            "status": status,
            "found_keywords": found_kws,
            "missing_keywords": missing_kws,
            "specific_feedback": company_feedback,
            "length_check": length_status
        }

ats_emulator = ATSEmulator()
