#!/usr/bin/env python3
"""Direct test of the resume analyzer"""
import warnings
warnings.filterwarnings('ignore')

print("Loading sample files...", flush=True)
with open("sample_resumes/sample_resume.txt", "r") as f:
    resume_text = f.read()

with open("sample_resumes/sample_job_description.txt", "r") as f:
    job_description = f.read()

print(f"Resume: {len(resume_text)} chars", flush=True)
print(f"Job Description: {len(job_description)} chars", flush=True)

print("\nImporting analyzer...", flush=True)
from backend.services.resume_analyzer import ResumeAnalyzer

print("Creating analyzer instance...", flush=True)
analyzer = ResumeAnalyzer()
print("Analyzer created!", flush=True)

print("\nPerforming analysis (this may take a moment)...", flush=True)
result = analyzer.analyze_resume(resume_text, job_description)

print("\n" + "="*80)
print("ANALYSIS RESULTS:")
print("="*80)
print(f"ATS Score: {result['ats_score']}/100")
print(f"Keyword Match Rate: {result['keyword_match_rate']:.1%}")
print(f"Matched Keywords: {len(result['matched_keywords'])} found")
print(f"  Sample: {', '.join(result['matched_keywords'][:5])}")
print(f"Missing Keywords: {len(result['missing_keywords'])} missing")
print(f"  Sample: {', '.join(result['missing_keywords'][:5])}")
print(f"\nSuggestions ({len(result['suggestions'])}):")
for i, suggestion in enumerate(result['suggestions'][:3], 1):
    print(f"  {i}. {suggestion}")
print("\n" + "="*80)
print("SUCCESS!")
