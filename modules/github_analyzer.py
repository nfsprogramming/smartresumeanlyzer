"""
GitHub Analyzer Module
Analyzes GitHub profiles to extract skills and project stats
"""

import streamlit as st
import pandas as pd
from github import Github, GithubException
from config import APIKeys
from collections import Counter

class GitHubAnalyzer:
    """
    Analyzes a GitHub profile for tech stack and activity.
    """
    
    def __init__(self):
        self.g = None
        # Use token if available to avoid rate limits
        token = APIKeys.GITHUB_TOKEN
        if token:
            self.g = Github(token)
        else:
            self.g = Github()

    def analyze_profile(self, username: str) -> dict:
        """
        Fetch and analyze user data.
        """
        try:
            user = self.g.get_user(username)
            
            # Basic Stats
            stats = {
                "name": user.name or username,
                "bio": user.bio,
                "repos": user.public_repos,
                "followers": user.followers,
                "avatar": user.avatar_url,
                "url": user.html_url,
                "created_at": user.created_at.year
            }
            
            # Analyze Repos
            repos = user.get_repos()
            languages = []
            topics = []
            top_projects = []
            
            # Limit to last 30 updated repos to be fast
            for repo in repos.get_page(0):
                if not repo.fork:
                    if repo.language:
                        languages.append(repo.language)
                    topics.extend(repo.get_topics())
                    
                    # Score repo based on stars + forks
                    score = repo.stargazers_count * 2 + repo.forks_count
                    if score > 0 or (repo.description and len(repo.description) > 50):
                        top_projects.append({
                            "name": repo.name,
                            "stars": repo.stargazers_count,
                            "language": repo.language,
                            "desc": repo.description,
                            "url": repo.html_url,
                            "score": score
                        })
            
            # Sort projects
            top_projects.sort(key=lambda x: x['score'], reverse=True)
            
            # Language Stats
            lang_counts = Counter(languages)
            total_langs = sum(lang_counts.values())
            lang_stats = {k: round((v/total_langs)*100, 1) for k, v in lang_counts.most_common(5)}
            
            return {
                "stats": stats,
                "languages": lang_stats,
                "topics": Counter(topics).most_common(10),
                "top_projects": top_projects[:5],
                "error": None
            }
            
        except GithubException as e:
            if e.status == 404:
                return {"error": "User not found"}
            elif e.status == 403:
                return {"error": "API Rate Limit Exceeded. Add GITHUB_TOKEN to .env"}
            return {"error": str(e)}
        except Exception as e:
            return {"error": str(e)}

github_analyzer = GitHubAnalyzer()
