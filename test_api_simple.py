#!/usr/bin/env python3
"""Test the API endpoint - simple version"""
import requests
import time

time.sleep(2)

with open("sample_resumes/sample_resume.txt", "r") as f:
    resume_text = f.read()

with open("sample_resumes/sample_job_description.txt", "r") as f:
    job_description = f.read()

print("Testing API: POST /api/analyze")

data = {
    "job_description": job_description,
    "resume_text": resume_text
}

try:
    response = requests.post(
        "http://127.0.0.1:8000/api/analyze",
        data=data,
        timeout=30
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"SUCCESS!")
        print(f"ATS Score: {result['ats_score']}/100")
        print(f"Keyword Match: {result['keyword_match_rate']}%")
        print(f"Matched Keywords: {len(result['matched_keywords'])}")
        print(f"Missing Keywords: {len(result['missing_keywords'])}")
    else:
        print(f"Error: {response.text[:200]}")
        
except Exception as e:
    print(f"Error: {str(e)[:100]}")
