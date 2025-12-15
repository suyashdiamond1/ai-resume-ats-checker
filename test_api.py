#!/usr/bin/env python3
import requests
import sys
import time

# Give server a moment to fully start
time.sleep(2)

# Read the sample files
with open("sample_resumes/sample_resume.txt", "r") as f:
    resume_text = f.read()

with open("sample_resumes/sample_job_description.txt", "r") as f:
    job_description = f.read()

print(f"Resume length: {len(resume_text)} chars")
print(f"Job description length: {len(job_description)} chars")
print("\n" + "="*80)

# Test 1: Text-based analysis
print("\nTest 1: Text-based analysis")
print("-" * 80)

try:
    response = requests.post(
        "http://localhost:8000/api/analyze",
        data={
            "job_description": job_description,
            "resume_text": resume_text
        },
        timeout=30
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"Response Body: {response.text[:500] if len(response.text) > 500 else response.text}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nAnalysis Results:")
        print(f"  ATS Score: {result.get('ats_score', 'N/A')}")
        print(f"  Keyword Match Rate: {result.get('keyword_match_rate', 'N/A')}")
        print(f"  Matched Keywords: {len(result.get('matched_keywords', []))} keywords")
        print(f"  Missing Keywords: {len(result.get('missing_keywords', []))} keywords")
        print(f"  Suggestions: {len(result.get('suggestions', []))} suggestions")
    else:
        print(f"\nError Response:")
        print(response.text)
        
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)

# Test 2: PDF file analysis
print("\nTest 2: PDF file analysis")
print("-" * 80)

try:
    # Check if a PDF sample exists
    import os
    pdf_files = [f for f in os.listdir("sample_resumes") if f.endswith(".pdf")]
    
    if pdf_files:
        pdf_file = pdf_files[0]
        with open(f"sample_resumes/{pdf_file}", "rb") as f:
            files = {
                "resume_file": (pdf_file, f, "application/pdf")
            }
            data = {
                "job_description": job_description
            }
            
            response = requests.post(
                "http://localhost:8000/api/analyze",
                files=files,
                data=data,
                timeout=30
            )
            
            print(f"Status Code: {response.status_code}")
            print(f"Response Body: {response.text[:500] if len(response.text) > 500 else response.text}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"\nAnalysis Results:")
                print(f"  ATS Score: {result.get('ats_score', 'N/A')}")
    else:
        print("No PDF files found in sample_resumes directory")
        
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
print("Testing complete!")
