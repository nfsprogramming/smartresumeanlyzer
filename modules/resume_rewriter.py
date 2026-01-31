"""
Resume Rewrite Engine Module
Uses LLMs via Central AI Engine to rewrite resume content
"""

from utils.llm_wrapper import ai_engine

class ResumeRewriter:
    """
    AI-powered resume rewriter using Central AI Engine.
    """
    
    def rewrite_section(self, section_text: str, target_role: str, tone: str = "Professional") -> str:
        """
        Rewrite a specific section for a target role (Sync).
        """
        prompt = f"""
        Act as an expert resume writer. Rewrite the following resume section to be optimized for a '{target_role}' position.
        
        Guidelines:
        - Tone: {tone}
        - Focus: Highlight skills relevant to {target_role}
        - Action Verbs: Use strong, dynamic verbs.
        - Clarity: Remove fluff.
        - Output: Provide ONLY the rewritten text.
        
        Original Text:
        "{section_text}"
        """
        
        return ai_engine.chat(prompt, system="You are a professional resume writer.")

    def generate_tailored_summary(self, resume_text: str, jd_text: str) -> str:
        """
        Generate a summary tailored to a JD.
        """
        prompt = f"""
        Draft a compelling Professional Summary (3-4 sentences) for a resume.
        
        Context:
        - Job Description Snippet: "{jd_text[:800]}..."
        - User Background Snippet: "{resume_text[:1000]}..."
        
        Goal:
        - Connect the candidate's skills to the job.
        - Use specific keywords from the JD.
        """
        
        return ai_engine.chat(prompt, system="You are a clear and persuasive career coach.")

resume_rewriter = ResumeRewriter()
