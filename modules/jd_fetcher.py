"""
JD Auto-Fetcher Module
Extracts job descriptions from URLs (LinkedIn, Indeed, Naukri, etc.)
"""

import requests
from bs4 import BeautifulSoup
import re
import streamlit as st
import time

class JDFetcher:
    """
    Fetches and parses job descriptions from various job board URLs.
    """
    
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }

    @staticmethod
    def identify_platform(url: str) -> str:
        """Identify the job platform from the URL."""
        if "linkedin.com" in url:
            return "LinkedIn"
        elif "indeed.com" in url or "indeed.co" in url:
            return "Indeed"
        elif "naukri.com" in url:
            return "Naukri"
        elif "glassdoor.com" in url:
            return "Glassdoor"
        else:
            return "Generic"

    def fetch_from_url(self, url: str) -> str:
        """
        Main method to fetch JD text from a URL.
        """
        if not url:
            return ""
            
        # Automatic URL correction: Add https:// if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        platform = self.identify_platform(url)
        
        # Warning for LinkedIn Profiles (common user error)
        if platform == "LinkedIn" and "/in/" in url:
            st.error("🚫 Error: You entered a LinkedIn Profile URL, not a Job Posting URL.")
            st.info("Please use a Job URL, for example: `https://www.linkedin.com/jobs/view/12345678`")
            return ""
        
        try:
            if platform == "LinkedIn":
                return self._scrape_linkedin(url)
            elif platform == "Indeed":
                return self._scrape_indeed(url)
            else:
                return self._scrape_generic(url)
        except Exception as e:
            if "999" in str(e):
                st.error("⚠️ LinkedIn blocked the request (Status 999). This is common with automated tools.")
                st.info("💡 Tip: Open the link in your browser, copy the text, and paste it manually into the analysis tool.")
            else:
                st.error(f"Error fetching JD from {platform}: {str(e)}")
            return ""

    def _scrape_linkedin(self, url: str) -> str:
        """
        Scrape public LinkedIn job posting.
        Note: LinkedIn creates dynamic classes. We target the specific description container.
        """
        # Clean URL to ensuring we get the public view if possible
        # Real scraping often requires Selenium/Playwright for heavy JS sites like LinkedIn, 
        # but the request method works for public-facing job pages sometimes.
        
        response = requests.get(url, headers=self.HEADERS)
        if response.status_code != 200:
            raise Exception(f"Status code {response.status_code}")
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try different common selectors for LinkedIn public jobs
        selectors = [
            'div.description__text', 
            'div.show-more-less-html__markup',
            'div.job-description'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return self._clean_html(element.get_text(separator="\n"))
                
        # Fallback: getting all text from main
        main = soup.find('main')
        if main:
            return self._clean_html(main.get_text(separator="\n"))
            
        return ""

    def _scrape_indeed(self, url: str) -> str:
        """Scrape Indeed job posting."""
        response = requests.get(url, headers=self.HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Indeed usually uses 'jobDescriptionText' id
        element = soup.find(id="jobDescriptionText")
        if element:
            return self._clean_html(element.get_text(separator="\n"))
            
        return ""

    def _scrape_generic(self, url: str) -> str:
        """Generic fallback scraper for other sites."""
        response = requests.get(url, headers=self.HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
            
        # Get text
        text = soup.get_text(separator="\n")
        
        # Simple heuristic: The JD is usually the largest block of text
        # or we return the whole body cleaned
        return self._clean_html(text)

    def _clean_html(self, text: str) -> str:
        """Clean up extracted text."""
        # Break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text

# Initialize global instance
jd_fetcher = JDFetcher()
