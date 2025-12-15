#!/usr/bin/env python3
"""Direct test of the resume analyzer - debug version"""
import warnings
warnings.filterwarnings('ignore')

from backend.services.resume_analyzer import ResumeAnalyzer

with open("sample_resumes/sample_resume.txt", "r") as f:
    resume_text = f.read()

with open("sample_resumes/sample_job_description.txt", "r") as f:
    job_description = f.read()

analyzer = ResumeAnalyzer()
result = analyzer.analyze_resume(resume_text, job_description)

print(f"keyword_match_rate value: {result['keyword_match_rate']}")
print(f"keyword_match_rate type: {type(result['keyword_match_rate'])}")
print(f"ats_score: {result['ats_score']}")
print(f"matched_keywords: {result['matched_keywords']}")
