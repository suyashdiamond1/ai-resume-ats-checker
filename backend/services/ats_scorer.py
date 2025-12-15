"""ATS Scoring Service - Core Analysis Engine"""
import re
from typing import List, Dict, Tuple, Set
from collections import Counter
import numpy as np


class ATSScorer:
    """ATS Scoring Engine using TF-IDF and NLP"""
    
    # Common resume sections keywords
    SECTION_KEYWORDS = {
        'skills': ['skills', 'technical skills', 'core competencies', 'expertise', 'proficiencies'],
        'experience': ['experience', 'work history', 'employment', 'professional experience', 'work experience'],
        'education': ['education', 'academic', 'degree', 'university', 'college', 'qualification']
    }
    
    def __init__(self):
        """Initialize the ATS Scorer"""
        self.nlp = None  # Lazy-load on first use
        self._tfidf_initialized = False
        self.tfidf_vectorizer = None  # Lazy-load on first use
    
    def _ensure_nlp_loaded(self):
        """Ensure spaCy model is loaded - using fallback if issues occur"""
        if self.nlp is None:
            try:
                # Suppress pydantic warnings during import
                import warnings
                warnings.filterwarnings('ignore', category=DeprecationWarning)
                
                import sys
                import os
                # Suppress pydantic v1 compatibility warnings
                os.environ["PYDANTIC_V1_COMPATIBILITY_MODE"] = "1"
                
                print("Loading spaCy model (this may take a moment)...")
                import spacy
                self.nlp = spacy.load("en_core_web_sm")
                print("spaCy model loaded successfully")
            except Exception as e:
                print(f"Note: Could not load spacy ({e}). Using fallback NLTK tokenization.")
                # Fallback mode - we'll use simple tokenization instead
                self.nlp = None
                self._use_fallback = True
    
    def _ensure_tfidf_loaded(self):
        """Ensure TF-IDF vectorizer is initialized"""
        if self.tfidf_vectorizer is None:
            from sklearn.feature_extraction.text import TfidfVectorizer
            self.tfidf_vectorizer = TfidfVectorizer(
                max_features=500,
                stop_words='english',
                ngram_range=(1, 2),  # Unigrams and bigrams
                min_df=1
            )
    
    def normalize_text(self, text: str) -> str:
        """Normalize text for analysis"""
        # Convert to lowercase
        text = text.lower()
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def extract_keywords(self, text: str, top_n: int = 50) -> List[str]:
        """
        Extract important keywords from text using NLP
        
        Args:
            text: Input text
            top_n: Number of top keywords to extract
            
        Returns:
            List of keywords
        """
        self._ensure_nlp_loaded()
        
        # Check if we're using spacy or fallback
        if self.nlp is None:
            # Fallback: Simple regex-based keyword extraction
            # Common English stopwords
            stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'is', 'are', 'was', 'were', 'be', 'have', 'has', 'had', 'do', 'does', 'did', 'that', 'this', 'which', 'who', 'what', 'where', 'when', 'why', 'how', 'as', 'from', 'by', 'up', 'about', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'between', 'under', 'again', 'further', 'then', 'once'}
            
            # Extract words
            words = re.findall(r'\b\w{3,}\b', text.lower())
            keywords = [w for w in words if w not in stop_words]
            keyword_counts = Counter(keywords)
            return [kw for kw, _ in keyword_counts.most_common(top_n)]
        
        # Use spacy if available
        try:
            doc = self.nlp(text.lower())
            
            # Extract nouns, proper nouns, and adjectives (skills, technologies, etc.)
            keywords = []
            for token in doc:
                if (token.pos_ in ['NOUN', 'PROPN', 'ADJ'] and 
                    not token.is_stop and 
                    len(token.text) > 2):
                    keywords.append(token.text)
            
            # Extract noun chunks (multi-word skills like "machine learning")
            for chunk in doc.noun_chunks:
                if len(chunk.text.split()) > 1:
                    keywords.append(chunk.text.lower())
            
            # Count frequency and return top keywords
            keyword_counts = Counter(keywords)
            return [kw for kw, _ in keyword_counts.most_common(top_n)]
        except:
            # Fallback to regex if spacy fails
            words = re.findall(r'\b\w{3,}\b', text.lower())
            keyword_counts = Counter(words)
            return [kw for kw, _ in keyword_counts.most_common(top_n)]
    
    def calculate_tfidf_similarity(self, resume_text: str, job_description: str) -> float:
        """
        Calculate TF-IDF cosine similarity between resume and job description
        
        Args:
            resume_text: Resume text
            job_description: Job description text
            
        Returns:
            Similarity score (0-1)
        """
        try:
            # Ensure vectorizer is loaded
            self._ensure_tfidf_loaded()
            
            # Create TF-IDF vectors
            from sklearn.metrics.pairwise import cosine_similarity
            tfidf_matrix = self.tfidf_vectorizer.fit_transform([resume_text, job_description])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return float(similarity)
        except Exception:
            return 0.0
    
    def find_keyword_matches(
        self, 
        resume_keywords: List[str], 
        job_keywords: List[str]
    ) -> Tuple[List[str], List[str], float]:
        """
        Find matched and missing keywords
        
        Args:
            resume_keywords: Keywords from resume
            job_keywords: Keywords from job description
            
        Returns:
            Tuple of (matched_keywords, missing_keywords, match_rate)
        """
        resume_set = set(resume_keywords)
        job_set = set(job_keywords)
        
        # Find exact matches
        matched = list(resume_set.intersection(job_set))
        
        # Find partial matches (substring matching for compound skills)
        partial_matches = []
        for job_kw in job_set:
            if job_kw not in matched:
                for resume_kw in resume_set:
                    if job_kw in resume_kw or resume_kw in job_kw:
                        partial_matches.append(job_kw)
                        break
        
        all_matched = matched + partial_matches
        missing = [kw for kw in job_set if kw not in all_matched]
        
        # Calculate match rate
        match_rate = len(all_matched) / len(job_set) if job_set else 0.0
        
        return all_matched, missing, match_rate
    
    def detect_sections(self, resume_text: str) -> Dict[str, bool]:
        """
        Detect presence of key resume sections
        
        Args:
            resume_text: Resume text
            
        Returns:
            Dictionary with section presence flags
        """
        text_lower = resume_text.lower()
        
        sections = {}
        for section_name, keywords in self.SECTION_KEYWORDS.items():
            sections[section_name] = any(keyword in text_lower for keyword in keywords)
        
        return sections
    
    def extract_skills(self, text: str) -> List[str]:
        """
        Extract technical skills and competencies
        
        Args:
            text: Input text
            
        Returns:
            List of identified skills
        """
        # Common technical skills patterns
        tech_skills_pattern = r'\b(python|java|javascript|react|angular|vue|node\.?js|docker|kubernetes|aws|azure|gcp|sql|nosql|mongodb|postgresql|git|ci/cd|agile|scrum|machine learning|deep learning|ai|data science|typescript|c\+\+|c#|golang|rust|scala|kotlin|swift|flutter|django|flask|fastapi|spring|\.net|tensorflow|pytorch|scikit-learn|pandas|numpy)\b'
        
        skills = re.findall(tech_skills_pattern, text.lower())
        
        # Also extract from noun phrases if spacy is available
        self._ensure_nlp_loaded()
        if self.nlp is not None:
            try:
                doc = self.nlp(text.lower())
                for chunk in doc.noun_chunks:
                    if len(chunk.text.split()) <= 3:  # Short phrases likely to be skills
                        skills.append(chunk.text)
            except:
                pass  # Ignore errors, we already have regex-based skills
        
        return list(set(skills))
    
    def generate_suggestions(
        self, 
        missing_keywords: List[str],
        section_analysis: Dict[str, bool],
        match_rate: float,
        ats_score: int
    ) -> List[str]:
        """
        Generate actionable improvement suggestions
        
        Args:
            missing_keywords: Keywords missing from resume
            section_analysis: Section presence analysis
            match_rate: Keyword match rate
            ats_score: Overall ATS score
            
        Returns:
            List of suggestions
        """
        suggestions = []
        
        # Score-based suggestions
        if ats_score < 40:
            suggestions.append("Your resume needs significant improvements to match this job description. Consider a major revision.")
        elif ats_score < 60:
            suggestions.append("Your resume shows moderate alignment. Focus on incorporating more relevant keywords.")
        elif ats_score < 80:
            suggestions.append("Good alignment! Add a few more relevant keywords to improve further.")
        else:
            suggestions.append("Excellent ATS compatibility! Your resume is well-optimized for this role.")
        
        # Keyword-based suggestions
        if missing_keywords:
            top_missing = missing_keywords[:5]
            suggestions.append(f"Add these important keywords: {', '.join(top_missing)}")
        
        # Section-based suggestions
        if not section_analysis.get('skills', False):
            suggestions.append("Add a dedicated 'Skills' or 'Technical Skills' section to improve ATS readability.")
        
        if not section_analysis.get('experience', False):
            suggestions.append("Ensure you have a clear 'Work Experience' or 'Professional Experience' section.")
        
        if not section_analysis.get('education', False):
            suggestions.append("Include an 'Education' section if you have relevant qualifications.")
        
        # Match rate suggestions
        if match_rate < 0.3:
            suggestions.append("Less than 30% keyword match. Tailor your resume more closely to the job description.")
        elif match_rate < 0.5:
            suggestions.append("Keyword match is below 50%. Review the job description and incorporate more relevant terms.")
        
        # General formatting suggestions
        suggestions.append("Use standard section headings (Skills, Experience, Education) for better ATS parsing.")
        suggestions.append("Include specific achievements with metrics where possible.")
        suggestions.append("Avoid tables, images, and complex formatting that ATS systems may not parse correctly.")
        
        return suggestions
    
    def analyze(self, resume_text: str, job_description: str) -> Dict:
        """
        Perform comprehensive ATS analysis
        
        Args:
            resume_text: Cleaned resume text
            job_description: Job description text
            
        Returns:
            Analysis results dictionary
        """
        # Normalize texts
        resume_normalized = self.normalize_text(resume_text)
        job_normalized = self.normalize_text(job_description)
        
        # Extract keywords
        resume_keywords = self.extract_keywords(resume_normalized)
        job_keywords = self.extract_keywords(job_normalized)
        
        # Find matches
        matched_keywords, missing_keywords, match_rate = self.find_keyword_matches(
            resume_keywords, 
            job_keywords
        )
        
        # Calculate TF-IDF similarity
        tfidf_score = self.calculate_tfidf_similarity(resume_normalized, job_normalized)
        
        # Detect sections
        section_analysis = self.detect_sections(resume_text)
        
        # Extract skills
        resume_skills = self.extract_skills(resume_text)
        job_skills = self.extract_skills(job_description)
        skill_gaps = [skill for skill in job_skills if skill not in resume_skills]
        
        # Calculate final ATS score (weighted combination)
        # 40% keyword match rate, 30% TF-IDF similarity, 30% section completeness
        section_score = sum(section_analysis.values()) / len(section_analysis)
        ats_score = int(
            (match_rate * 0.4 + tfidf_score * 0.3 + section_score * 0.3) * 100
        )
        ats_score = min(100, max(0, ats_score))  # Clamp to 0-100
        
        # Generate suggestions
        suggestions = self.generate_suggestions(
            missing_keywords,
            section_analysis,
            match_rate,
            ats_score
        )
        
        return {
            'ats_score': ats_score,
            'matched_keywords': matched_keywords[:20],  # Top 20
            'missing_keywords': missing_keywords[:15],  # Top 15
            'section_analysis': section_analysis,
            'suggestions': suggestions,
            'keyword_match_rate': round(match_rate * 100, 2),
            'skill_gaps': skill_gaps[:10]  # Top 10
        }
