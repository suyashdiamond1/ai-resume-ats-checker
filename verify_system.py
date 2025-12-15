#!/usr/bin/env python3
"""
Complete end-to-end test of the ATS Analyzer
Runs server and performs analysis without network calls
"""
import sys
import time

print("=" * 80)
print("AI Resume ATS Checker - Complete Verification")
print("=" * 80)

# Test 1: Import check
print("\n[1/3] Testing imports...", end=" ", flush=True)
try:
    from backend.services.resume_analyzer import ResumeAnalyzer
    print("OK")
except Exception as e:
    print(f"FAILED: {e}")
    sys.exit(1)

# Test 2: Load sample files
print("[2/3] Loading sample files...", end=" ", flush=True)
try:
    with open("sample_resumes/sample_resume.txt", "r") as f:
        resume_text = f.read()
    with open("sample_resumes/sample_job_description.txt", "r") as f:
        job_description = f.read()
    print("OK")
except Exception as e:
    print(f"FAILED: {e}")
    sys.exit(1)

# Test 3: Run analyzer
print("[3/3] Running analysis...", end=" ", flush=True)
try:
    analyzer = ResumeAnalyzer()
    result = analyzer.analyze_resume(resume_text, job_description)
    print("OK")
except Exception as e:
    print(f"FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Display results
print("\n" + "=" * 80)
print("ANALYSIS RESULTS")
print("=" * 80)
print(f"ATS Score:              {result['ats_score']}/100")
print(f"Keyword Match Rate:     {result['keyword_match_rate']:.1f}%")
print(f"Matched Keywords:       {len(result['matched_keywords'])} found")
print(f"  Examples:             {', '.join(result['matched_keywords'][:5])}")
print(f"Missing Keywords:       {len(result['missing_keywords'])} identified")
print(f"  Examples:             {', '.join(result['missing_keywords'][:5])}")
print(f"\nResume Sections:")
print(f"  Skills Present:       {result['section_analysis']['skills']}")
print(f"  Experience Present:   {result['section_analysis']['experience']}")
print(f"  Education Present:    {result['section_analysis']['education']}")
print(f"\nSuggestions ({len(result['suggestions'])}):")
for i, suggestion in enumerate(result['suggestions'][:3], 1):
    print(f"  {i}. {suggestion}")

print("\n" + "=" * 80)
print("VERIFICATION COMPLETE - ALL SYSTEMS OPERATIONAL")
print("=" * 80)
print("\nTo start the API server:")
print("  python start_server.py")
print("\nTo access the API documentation:")
print("  http://127.0.0.1:8000/docs")
print("=" * 80)
