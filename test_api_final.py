#!/usr/bin/env python3
"""Test the API endpoint"""
import requests
import json
import time

time.sleep(2)  # Wait for server to be ready

# Read sample files
with open("sample_resumes/sample_resume.txt", "r") as f:
    resume_text = f.read()

with open("sample_resumes/sample_job_description.txt", "r") as f:
    job_description = f.read()

print("=" * 80)
print("Testing API: POST /api/analyze")
print("=" * 80)

# Test with text resume
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
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response Headers Content-Type: {response.headers.get('content-type')}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ SUCCESS - Analysis Complete!")
        print(f"\nResults:")
        print(f"  ATS Score: {result['ats_score']}/100")
        print(f"  Keyword Match Rate: {result['keyword_match_rate']:.1f}%")
        print(f"  Matched Keywords ({len(result['matched_keywords'])}): {', '.join(result['matched_keywords'][:5])}...")
        print(f"  Missing Keywords ({len(result['missing_keywords'])}): {', '.join(result['missing_keywords'][:5])}...")
        print(f"  Sections: Skills={result['section_analysis']['skills']}, Experience={result['section_analysis']['experience']}, Education={result['section_analysis']['education']}")
        print(f"  Suggestions ({len(result['suggestions'])}):")
        for i, sug in enumerate(result['suggestions'][:3], 1):
            print(f"    {i}. {sug}")
    else:
        print(f"\n❌ ERROR - Status {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
