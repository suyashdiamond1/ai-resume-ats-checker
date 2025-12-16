"""ATS Scoring Service - Advanced Analysis Engine with Claude-level Accuracy"""
import re
from typing import List, Dict, Tuple, Set, Optional
from collections import Counter, defaultdict
import numpy as np
from datetime import datetime


class ATSScorer:
    """
    Advanced ATS Scoring Engine with multi-dimensional analysis:
    - Semantic similarity using embeddings
    - Contextual keyword matching
    - Experience relevance scoring
    - Skills depth analysis
    - Industry-specific terminology
    - Achievement impact assessment
    """
    
    # Comprehensive resume sections with variations
    SECTION_KEYWORDS = {
        'skills': ['skills', 'technical skills', 'core competencies', 'expertise', 'proficiencies', 
                   'technologies', 'tools', 'technical proficiencies', 'key skills'],
        'experience': ['experience', 'work history', 'employment', 'professional experience', 
                      'work experience', 'career history', 'employment history', 'professional background'],
        'education': ['education', 'academic', 'degree', 'university', 'college', 'qualification',
                     'academic background', 'certifications', 'training'],
        'achievements': ['achievements', 'accomplishments', 'awards', 'honors', 'recognition'],
        'projects': ['projects', 'portfolio', 'key projects', 'notable work']
    }
    
    # Action verbs indicating strong experience
    ACTION_VERBS = {
        'leadership': ['led', 'managed', 'directed', 'supervised', 'coordinated', 'headed', 'spearheaded', 'orchestrated'],
        'achievement': ['achieved', 'accomplished', 'delivered', 'exceeded', 'surpassed', 'completed', 'attained'],
        'improvement': ['improved', 'enhanced', 'optimized', 'increased', 'reduced', 'streamlined', 'accelerated', 'maximized'],
        'creation': ['created', 'developed', 'designed', 'built', 'implemented', 'established', 'launched', 'pioneered'],
        'collaboration': ['collaborated', 'partnered', 'coordinated', 'facilitated', 'contributed', 'supported']
    }
    
    # Quantifiable metrics patterns
    METRIC_PATTERNS = [
        r'\d+%',  # Percentages
        r'\$\d+[kKmMbB]?',  # Money
        r'\d+[kKmMbB]\+?',  # Large numbers
        r'\d+x',  # Multipliers
        r'\d+\s*(years?|months?|weeks?)',  # Time periods
        r'\d+\s*(users?|customers?|clients?|people|employees|team members?)',  # Scale
    ]
    
    def __init__(self):
        """Initialize the Advanced ATS Scorer"""
        self.nlp = None  # Lazy-load on first use
        self._tfidf_initialized = False
        self.tfidf_vectorizer = None  # Lazy-load on first use
        self._use_fallback = False
        self.sentence_model = None  # For semantic similarity
        self._embeddings_cache = {}  # Cache for embeddings
    
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
        """Ensure TF-IDF vectorizer is initialized with optimal parameters"""
        if self.tfidf_vectorizer is None:
            from sklearn.feature_extraction.text import TfidfVectorizer
            self.tfidf_vectorizer = TfidfVectorizer(
                max_features=1000,  # Increased for better coverage
                stop_words='english',
                ngram_range=(1, 3),  # Unigrams, bigrams, and trigrams
                min_df=1,
                max_df=0.95,  # Ignore terms that appear in >95% of documents
                sublinear_tf=True  # Use logarithmic TF scaling
            )
    
    def _ensure_embeddings_loaded(self):
        """Ensure sentence transformer model is loaded for semantic similarity"""
        if self.sentence_model is None:
            try:
                from sentence_transformers import SentenceTransformer
                print("Loading semantic model for deep analysis...")
                self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
                print("Semantic model loaded successfully")
            except Exception as e:
                print(f"Note: Semantic embeddings unavailable ({e}). Using TF-IDF fallback.")
                self.sentence_model = False  # Mark as unavailable
    
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
        Extract technical and soft skills with comprehensive coverage
        
        Args:
            text: Input text
            
        Returns:
            List of identified skills
        """
        # Comprehensive technical skills patterns (expanded significantly)
        tech_patterns = {
            'programming': r'\b(python|java|javascript|typescript|c\+\+|c#|golang|go|rust|scala|kotlin|swift|ruby|php|perl|r|matlab|julia|dart|flutter|react native|objective-c)\b',
            'web_frontend': r'\b(react|angular|vue|svelte|next\.?js|nuxt|ember|backbone|jquery|html5?|css3?|sass|scss|less|tailwind|bootstrap|material ui|webpack|vite|parcel)\b',
            'web_backend': r'\b(node\.?js|express|django|flask|fastapi|spring boot?|spring|\.net|asp\.net|rails|laravel|symfony|nestjs|koa|hapi)\b',
            'mobile': r'\b(ios|android|react native|flutter|xamarin|ionic|cordova|swift|kotlin|objective-c|swiftui)\b',
            'databases': r'\b(sql|nosql|mysql|postgresql|postgres|mongodb|cassandra|redis|elasticsearch|dynamodb|oracle|sql server|mariadb|couchdb|neo4j|graph database)\b',
            'cloud': r'\b(aws|azure|gcp|google cloud|cloud platform|heroku|digitalocean|lambda|ec2|s3|cloudfront|cloud functions|cloud run|kubernetes|k8s|docker|containers|serverless)\b',
            'devops': r'\b(docker|kubernetes|k8s|jenkins|gitlab ci|github actions|circle ci|travis|terraform|ansible|puppet|chef|ci/cd|continuous integration|continuous deployment|devops)\b',
            'data_science': r'\b(machine learning|deep learning|ai|artificial intelligence|data science|data analysis|tensorflow|pytorch|keras|scikit-learn|pandas|numpy|scipy|jupyter|data visualization|statistics|nlp|computer vision|neural networks?)\b',
            'tools': r'\b(git|github|gitlab|bitbucket|jira|confluence|slack|trello|asana|vs code|visual studio|intellij|eclipse|postman|swagger|figma|sketch|adobe xd)\b',
            'methodologies': r'\b(agile|scrum|kanban|waterfall|devops|tdd|test[- ]driven|bdd|ci/cd|microservices|rest|restful|graphql|api|soap|mvc|mvvm|solid|design patterns?)\b',
            'soft_skills': r'\b(leadership|communication|problem[- ]solving|analytical|critical thinking|team work|collaboration|project management|time management|adaptability|creativity|mentoring|presentation)\b'
        }
        
        skills = []
        text_lower = text.lower()
        
        # Extract using all patterns
        for category, pattern in tech_patterns.items():
            found = re.findall(pattern, text_lower)
            skills.extend(found)
        
        # Also extract from noun phrases if spacy is available
        self._ensure_nlp_loaded()
        if self.nlp is not None and not self._use_fallback:
            try:
                doc = self.nlp(text_lower)
                for chunk in doc.noun_chunks:
                    chunk_text = chunk.text.strip()
                    # Skills are typically 1-4 words
                    if 1 <= len(chunk_text.split()) <= 4:
                        # Filter out common non-skill phrases
                        if not any(x in chunk_text for x in ['the ', 'this ', 'that ', 'these ', 'those ']):
                            skills.append(chunk_text)
            except:
                pass  # Ignore errors, we already have regex-based skills
        
        # Remove duplicates while preserving order
        seen = set()
        unique_skills = []
        for skill in skills:
            skill_normalized = skill.strip().lower()
            if skill_normalized and skill_normalized not in seen and len(skill_normalized) > 1:
                seen.add(skill_normalized)
                unique_skills.append(skill_normalized)
        
        return unique_skills
    
    def calculate_semantic_similarity(self, resume_text: str, job_description: str) -> float:
        """
        Calculate semantic similarity using sentence embeddings
        More accurate than TF-IDF for understanding meaning
        
        Args:
            resume_text: Resume text
            job_description: Job description text
            
        Returns:
            Similarity score (0-1)
        """
        self._ensure_embeddings_loaded()
        
        if self.sentence_model and self.sentence_model is not False:
            try:
                # Generate embeddings
                resume_embedding = self.sentence_model.encode(resume_text, show_progress_bar=False)
                job_embedding = self.sentence_model.encode(job_description, show_progress_bar=False)
                
                # Calculate cosine similarity
                from sklearn.metrics.pairwise import cosine_similarity
                similarity = cosine_similarity(
                    resume_embedding.reshape(1, -1),
                    job_embedding.reshape(1, -1)
                )[0][0]
                
                return float(similarity)
            except Exception as e:
                print(f"Semantic similarity calculation failed: {e}")
                return self.calculate_tfidf_similarity(resume_text, job_description)
        else:
            # Fallback to TF-IDF
            return self.calculate_tfidf_similarity(resume_text, job_description)
    
    def analyze_experience_depth(self, text: str) -> Dict:
        """
        Analyze the depth and quality of experience descriptions
        
        Args:
            text: Resume text
            
        Returns:
            Experience analysis metrics
        """
        text_lower = text.lower()
        
        # Count action verbs by category
        action_verb_counts = defaultdict(int)
        for category, verbs in self.ACTION_VERBS.items():
            for verb in verbs:
                action_verb_counts[category] += len(re.findall(r'\b' + verb + r'\b', text_lower))
        
        # Count quantifiable achievements
        metric_count = 0
        for pattern in self.METRIC_PATTERNS:
            metric_count += len(re.findall(pattern, text, re.IGNORECASE))
        
        # Calculate experience strength score
        total_action_verbs = sum(action_verb_counts.values())
        has_leadership = action_verb_counts['leadership'] > 0
        has_achievements = action_verb_counts['achievement'] > 0
        has_metrics = metric_count > 0
        
        # Experience strength: 0-100
        experience_score = min(100, (
            (total_action_verbs * 5) +  # Each action verb adds value
            (metric_count * 10) +  # Metrics are highly valuable
            (20 if has_leadership else 0) +
            (15 if has_achievements else 0)
        ))
        
        return {
            'action_verb_count': total_action_verbs,
            'metric_count': metric_count,
            'leadership_indicators': action_verb_counts['leadership'],
            'achievement_indicators': action_verb_counts['achievement'],
            'improvement_indicators': action_verb_counts['improvement'],
            'experience_strength_score': min(100, experience_score),
            'has_quantifiable_results': has_metrics
        }
    
    def analyze_keyword_context(self, resume_text: str, job_description: str, keywords: List[str]) -> Dict:
        """
        Analyze how keywords are used in context (not just presence)
        
        Args:
            resume_text: Resume text
            job_description: Job description text
            keywords: Keywords to analyze
            
        Returns:
            Context analysis results
        """
        resume_lower = resume_text.lower()
        job_lower = job_description.lower()
        
        context_scores = {}
        
        for keyword in keywords[:20]:  # Analyze top 20 keywords
            # Find keyword in context (surrounding words)
            resume_contexts = self._extract_keyword_contexts(resume_lower, keyword)
            job_contexts = self._extract_keyword_contexts(job_lower, keyword)
            
            if resume_contexts and job_contexts:
                # Calculate context similarity
                context_similarity = self._calculate_context_overlap(resume_contexts, job_contexts)
                context_scores[keyword] = context_similarity
            elif resume_contexts:
                context_scores[keyword] = 0.5  # Present but different context
            else:
                context_scores[keyword] = 0.0  # Not present
        
        # Average context score
        avg_context_score = np.mean(list(context_scores.values())) if context_scores else 0.0
        
        return {
            'context_scores': context_scores,
            'average_context_match': float(avg_context_score),
            'well_contextualized_keywords': sum(1 for score in context_scores.values() if score > 0.6)
        }
    
    def _extract_keyword_contexts(self, text: str, keyword: str, window: int = 5) -> List[str]:
        """Extract words surrounding a keyword"""
        words = text.split()
        contexts = []
        
        for i, word in enumerate(words):
            if keyword in word:
                start = max(0, i - window)
                end = min(len(words), i + window + 1)
                context = ' '.join(words[start:end])
                contexts.append(context)
        
        return contexts
    
    def _calculate_context_overlap(self, contexts1: List[str], contexts2: List[str]) -> float:
        """Calculate how similar the contexts are"""
        if not contexts1 or not contexts2:
            return 0.0
        
        # Get words from all contexts
        words1 = set(' '.join(contexts1).split())
        words2 = set(' '.join(contexts2).split())
        
        # Calculate Jaccard similarity
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0
    
    def analyze_skills_depth(self, resume_skills: List[str], job_skills: List[str]) -> Dict:
        """
        Analyze skill coverage and depth
        
        Args:
            resume_skills: Skills from resume
            job_skills: Required skills from job
            
        Returns:
            Skills depth analysis
        """
        resume_set = set(skill.lower() for skill in resume_skills)
        job_set = set(skill.lower() for skill in job_skills)
        
        # Exact matches
        exact_matches = resume_set.intersection(job_set)
        
        # Partial matches (related skills)
        partial_matches = set()
        for job_skill in job_set:
            if job_skill not in exact_matches:
                for resume_skill in resume_set:
                    if (job_skill in resume_skill or resume_skill in job_skill or
                        self._are_skills_related(job_skill, resume_skill)):
                        partial_matches.add(job_skill)
                        break
        
        # Missing critical skills
        missing_skills = job_set - exact_matches - partial_matches
        
        # Coverage calculation
        total_required = len(job_set)
        if total_required > 0:
            exact_coverage = len(exact_matches) / total_required
            partial_coverage = len(partial_matches) / total_required
            total_coverage = (len(exact_matches) + len(partial_matches)) / total_required
        else:
            exact_coverage = partial_coverage = total_coverage = 0.0
        
        return {
            'exact_skill_matches': list(exact_matches),
            'partial_skill_matches': list(partial_matches),
            'missing_skills': list(missing_skills),
            'exact_coverage': round(exact_coverage * 100, 2),
            'total_coverage': round(total_coverage * 100, 2),
            'skill_match_score': int(total_coverage * 100)
        }
    
    def _are_skills_related(self, skill1: str, skill2: str) -> bool:
        """Check if two skills are related"""
        # Define skill relationships
        skill_families = [
            {'python', 'django', 'flask', 'fastapi', 'pandas', 'numpy'},
            {'javascript', 'typescript', 'react', 'angular', 'vue', 'node.js', 'nodejs'},
            {'aws', 'azure', 'gcp', 'cloud', 'lambda', 'ec2', 's3'},
            {'docker', 'kubernetes', 'k8s', 'containers', 'devops'},
            {'sql', 'mysql', 'postgresql', 'database', 'nosql', 'mongodb'},
            {'machine learning', 'deep learning', 'ai', 'tensorflow', 'pytorch', 'data science'},
        ]
        
        for family in skill_families:
            if skill1 in family and skill2 in family:
                return True
        
        return False
    
    def generate_suggestions(
        self, 
        missing_keywords: List[str],
        section_analysis: Dict[str, bool],
        match_rate: float,
        ats_score: int,
        experience_analysis: Optional[Dict] = None,
        skills_analysis: Optional[Dict] = None,
        context_analysis: Optional[Dict] = None
    ) -> List[str]:
        """
        Generate highly specific and actionable improvement suggestions
        
        Args:
            missing_keywords: Keywords missing from resume
            section_analysis: Section presence analysis
            match_rate: Keyword match rate
            ats_score: Overall ATS score
            experience_analysis: Experience depth analysis
            skills_analysis: Skills depth analysis
            context_analysis: Keyword context analysis
            
        Returns:
            Prioritized list of suggestions
        """
        suggestions = []
        
        # Score-based guidance (more nuanced)
        if ats_score >= 90:
            suggestions.append("🌟 Outstanding! Your resume is exceptionally well-aligned with this role.")
        elif ats_score >= 80:
            suggestions.append("✅ Excellent match! Your resume shows strong alignment with the job requirements.")
        elif ats_score >= 70:
            suggestions.append("👍 Good alignment. A few targeted improvements will strengthen your application.")
        elif ats_score >= 60:
            suggestions.append("⚠️ Moderate match. Focus on incorporating more relevant keywords and skills.")
        elif ats_score >= 50:
            suggestions.append("⚠️ Below average alignment. Significant revisions needed to match this role.")
        else:
            suggestions.append("❌ Low compatibility. Consider major revisions or whether this role matches your background.")
        
        # Advanced experience-based suggestions
        if experience_analysis:
            if experience_analysis['metric_count'] < 3:
                suggestions.append("📊 Add quantifiable achievements with metrics (e.g., 'Increased efficiency by 40%', 'Managed team of 12', '$2M budget').")
            
            if experience_analysis['action_verb_count'] < 10:
                suggestions.append("💪 Use more strong action verbs (led, developed, improved, achieved, etc.) to describe your experience.")
            
            if experience_analysis['leadership_indicators'] == 0 and 'lead' in ' '.join(missing_keywords).lower():
                suggestions.append("👥 Emphasize leadership experience if applicable (led teams, managed projects, mentored others).")
            
            if experience_analysis['experience_strength_score'] < 50:
                suggestions.append("📝 Strengthen your experience descriptions with specific accomplishments and measurable impact.")
        
        # Skills-based suggestions
        if skills_analysis:
            if skills_analysis['total_coverage'] < 50:
                suggestions.append(f"🎯 Critical: Only {skills_analysis['total_coverage']:.0f}% skill match. Prioritize adding these missing skills to your resume.")
            
            if skills_analysis['missing_skills']:
                top_missing_skills = skills_analysis['missing_skills'][:5]
                suggestions.append(f"🔧 Add these key skills if you have them: {', '.join(top_missing_skills)}")
        
        # Context-based suggestions
        if context_analysis:
            if context_analysis['average_context_match'] < 0.4:
                suggestions.append("📖 Your keywords appear in different contexts than the job description. Align your phrasing more closely.")
            
            if context_analysis['well_contextualized_keywords'] < 5:
                suggestions.append("🎯 Use job description terminology more precisely to show direct relevance.")
        
        # Keyword-based suggestions (prioritized)
        if missing_keywords:
            critical_keywords = [kw for kw in missing_keywords[:10] if len(kw) > 3]
            if len(critical_keywords) >= 5:
                suggestions.append(f"🔑 High-priority keywords to add: {', '.join(critical_keywords[:5])}")
            elif critical_keywords:
                suggestions.append(f"🔑 Important keywords to incorporate: {', '.join(critical_keywords)}")
        
        # Section-based suggestions
        missing_sections = [section for section, present in section_analysis.items() if not present]
        if missing_sections:
            section_names = ', '.join(missing_sections).title()
            suggestions.append(f"📋 Add missing sections: {section_names}")
        
        if not section_analysis.get('skills', False):
            suggestions.append("💼 Create a dedicated 'Technical Skills' or 'Core Competencies' section for better ATS parsing.")
        
        if not section_analysis.get('achievements', False):
            suggestions.append("🏆 Consider adding an 'Achievements' or 'Key Accomplishments' section to highlight your impact.")
        
        # Match rate specific guidance
        if match_rate < 0.3:
            suggestions.append("⚠️ Very low keyword overlap (< 30%). This resume may not pass initial ATS screening.")
        elif match_rate < 0.5:
            suggestions.append("📈 Boost keyword match rate from {:.0f}% to at least 50% by tailoring content to job description.".format(match_rate * 100))
        
        # Advanced formatting and optimization
        suggestions.append("✨ Use industry-standard section headers (Professional Experience, Technical Skills, Education).")
        suggestions.append("📄 Avoid tables, text boxes, headers/footers, and images - ATS systems struggle with these.")
        suggestions.append("🔤 Use standard fonts (Arial, Calibri, Times New Roman) and save as .docx or PDF for best compatibility.")
        suggestions.append("🎯 Mirror the job description's language and terminology throughout your resume.")
        
        # Final strategic advice
        if ats_score < 70:
            suggestions.append("💡 Pro tip: Create a master resume with all your skills/experience, then customize for each application.")
        
        return suggestions
    
    def analyze(self, resume_text: str, job_description: str) -> Dict:
        """
        Perform comprehensive multi-dimensional ATS analysis
        Uses advanced NLP, semantic similarity, and contextual understanding
        
        Args:
            resume_text: Cleaned resume text
            job_description: Job description text
            
        Returns:
            Detailed analysis results with actionable insights
        """
        print("\n🔍 Starting advanced ATS analysis...")
        
        # Normalize texts
        resume_normalized = self.normalize_text(resume_text)
        job_normalized = self.normalize_text(job_description)
        
        # 1. Keyword Analysis
        print("📊 Extracting and analyzing keywords...")
        resume_keywords = self.extract_keywords(resume_normalized, top_n=100)
        job_keywords = self.extract_keywords(job_normalized, top_n=100)
        
        matched_keywords, missing_keywords, keyword_match_rate = self.find_keyword_matches(
            resume_keywords, 
            job_keywords
        )
        
        # 2. Semantic Similarity Analysis
        print("🧠 Computing semantic similarity...")
        semantic_score = self.calculate_semantic_similarity(resume_normalized, job_normalized)
        
        # 3. TF-IDF Analysis (as backup/complement)
        print("📈 Calculating TF-IDF similarity...")
        tfidf_score = self.calculate_tfidf_similarity(resume_normalized, job_normalized)
        
        # Use semantic if available, otherwise TF-IDF
        content_similarity = semantic_score if semantic_score > 0 else tfidf_score
        
        # 4. Skills Analysis
        print("🔧 Analyzing skills coverage...")
        resume_skills = self.extract_skills(resume_text)
        job_skills = self.extract_skills(job_description)
        skills_analysis = self.analyze_skills_depth(resume_skills, job_skills)
        
        # 5. Experience Depth Analysis
        print("💼 Evaluating experience quality...")
        experience_analysis = self.analyze_experience_depth(resume_text)
        
        # 6. Context Analysis
        print("🎯 Analyzing keyword context...")
        context_analysis = self.analyze_keyword_context(
            resume_text, 
            job_description, 
            job_keywords
        )
        
        # 7. Section Detection
        print("📋 Detecting resume sections...")
        section_analysis = self.detect_sections(resume_text)
        section_completeness = sum(section_analysis.values()) / len(section_analysis)
        
        # 8. Calculate Multi-Dimensional ATS Score
        print("🎯 Computing final ATS score...")
        
        # Weighted scoring components:
        weights = {
            'keyword_match': 0.25,      # 25% - Direct keyword matching
            'content_similarity': 0.25,  # 25% - Semantic/TF-IDF similarity
            'skills_coverage': 0.20,     # 20% - Skills match
            'experience_quality': 0.15,  # 15% - Experience depth
            'context_alignment': 0.10,   # 10% - Contextual usage
            'section_structure': 0.05    # 5%  - Resume structure
        }
        
        # Normalize all scores to 0-1 range
        normalized_scores = {
            'keyword_match': keyword_match_rate,
            'content_similarity': content_similarity,
            'skills_coverage': skills_analysis['total_coverage'] / 100,
            'experience_quality': experience_analysis['experience_strength_score'] / 100,
            'context_alignment': context_analysis['average_context_match'],
            'section_structure': section_completeness
        }
        
        # Calculate weighted average
        ats_score = sum(
            normalized_scores[component] * weight 
            for component, weight in weights.items()
        ) * 100
        
        # Apply bonuses and penalties
        # Bonus for quantifiable achievements
        if experience_analysis['metric_count'] >= 5:
            ats_score += 3
        elif experience_analysis['metric_count'] >= 3:
            ats_score += 2
        
        # Bonus for strong action verbs
        if experience_analysis['action_verb_count'] >= 15:
            ats_score += 2
        
        # Penalty for very short resume (likely incomplete)
        if len(resume_text) < 500:
            ats_score -= 10
        
        # Penalty for missing critical sections
        if not section_analysis.get('experience', False):
            ats_score -= 5
        if not section_analysis.get('skills', False):
            ats_score -= 5
        
        # Clamp to 0-100
        ats_score = int(min(100, max(0, ats_score)))
        
        # 9. Generate Intelligent Suggestions
        print("💡 Generating personalized suggestions...")
        suggestions = self.generate_suggestions(
            missing_keywords,
            section_analysis,
            keyword_match_rate,
            ats_score,
            experience_analysis,
            skills_analysis,
            context_analysis
        )
        
        print(f"✅ Analysis complete! ATS Score: {ats_score}/100\n")
        
        # Return comprehensive results
        return {
            # Core Metrics
            'ats_score': ats_score,
            'keyword_match_rate': round(keyword_match_rate * 100, 2),
            'semantic_similarity': round(semantic_score * 100, 2) if semantic_score > 0 else None,
            'tfidf_similarity': round(tfidf_score * 100, 2),
            'content_similarity_score': round(content_similarity * 100, 2),
            
            # Keywords
            'matched_keywords': matched_keywords[:25],
            'missing_keywords': missing_keywords[:20],
            'total_job_keywords': len(job_keywords),
            'total_resume_keywords': len(resume_keywords),
            
            # Skills Analysis
            'skills_analysis': {
                'exact_matches': skills_analysis['exact_skill_matches'][:15],
                'partial_matches': skills_analysis['partial_skill_matches'][:10],
                'missing_skills': skills_analysis['missing_skills'][:15],
                'exact_coverage_percent': skills_analysis['exact_coverage'],
                'total_coverage_percent': skills_analysis['total_coverage'],
                'skill_match_score': skills_analysis['skill_match_score']
            },
            
            # Experience Analysis
            'experience_analysis': {
                'action_verb_count': experience_analysis['action_verb_count'],
                'quantifiable_achievements': experience_analysis['metric_count'],
                'leadership_indicators': experience_analysis['leadership_indicators'],
                'achievement_indicators': experience_analysis['achievement_indicators'],
                'experience_strength_score': experience_analysis['experience_strength_score'],
                'has_measurable_impact': experience_analysis['has_quantifiable_results']
            },
            
            # Context Analysis
            'context_analysis': {
                'average_context_match': round(context_analysis['average_context_match'] * 100, 2),
                'well_contextualized_count': context_analysis['well_contextualized_keywords']
            },
            
            # Structure Analysis
            'section_analysis': section_analysis,
            'section_completeness_percent': round(section_completeness * 100, 2),
            
            # Score Breakdown (for transparency)
            'score_breakdown': {
                component: {
                    'weight_percent': int(weight * 100),
                    'score': round(normalized_scores[component] * 100, 2),
                    'contribution': round(normalized_scores[component] * weight * 100, 2)
                }
                for component, weight in weights.items()
            },
            
            # Actionable Suggestions
            'suggestions': suggestions,
            
            # Metadata
            'analysis_timestamp': datetime.now().isoformat(),
            'resume_length': len(resume_text),
            'job_description_length': len(job_description)
        }
