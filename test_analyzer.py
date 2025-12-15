#!/usr/bin/env python
"""Test script for Resume ATS Analyzer"""

from backend.services.resume_analyzer import ResumeAnalyzer

# Test with sample files
try:
    print("Loading sample files...")
    with open('sample_resumes/sample_resume.txt', 'r') as f:
        resume_text = f.read()

    with open('sample_resumes/sample_job_description.txt', 'r') as f:
        job_desc = f.read()

    print("Creating analyzer...")
    analyzer = ResumeAnalyzer()
    
    print("Running analysis...")
    result = analyzer.analyze_resume(resume_text, job_desc)
    
    print("\n✅ ANALYSIS SUCCESSFUL!\n")
    print(f"ATS Score: {result['ats_score']}/100")
    print(f"Keyword Match Rate: {result['keyword_match_rate']}%")
    print(f"\nMatched Keywords: {result['matched_keywords'][:5]}")
    print(f"Missing Keywords: {result['missing_keywords'][:5]}")
    print(f"\nSuggestions:")
    for i, suggestion in enumerate(result['suggestions'][:3], 1):
        print(f"  {i}. {suggestion}")
        
except Exception as e:
    print(f"❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
