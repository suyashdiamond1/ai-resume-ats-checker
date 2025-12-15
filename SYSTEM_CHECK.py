#!/usr/bin/env python3
"""
COMPREHENSIVE SYSTEM CHECK & API TEST
This script tests that the entire system works correctly
"""
import sys
import warnings
warnings.filterwarnings('ignore')

print("\n" + "="*80)
print("AI RESUME ATS CHECKER - COMPREHENSIVE SYSTEM TEST")
print("="*80)

# Test 1: Analyzer works
print("\n[TEST 1] Testing Analyzer Engine...")
try:
    from backend.services.resume_analyzer import ResumeAnalyzer
    
    analyzer = ResumeAnalyzer()
    test_result = analyzer.analyze_resume(
        "Python Developer with 5 years experience in Django REST frameworks building scalable web applications. Experience with PostgreSQL, Redis, and AWS deployment.",
        "Senior Python Developer Required with Django experience and cloud deployment knowledge"
    )
    
    assert test_result['ats_score'] > 0
    assert test_result['keyword_match_rate'] >= 0
    print("  [OK] Analyzer working correctly")
except Exception as e:
    print(f"  [FAIL] Analyzer failed: {e}")
    sys.exit(1)

# Test 2: FastAPI app loads
print("[TEST 2] Testing FastAPI Application...")
try:
    from backend.main import app
    print("  [OK] FastAPI app loaded successfully")
except Exception as e:
    print(f"  [FAIL] FastAPI app failed: {e}")
    sys.exit(1)

# Test 3: Test with actual sample files
print("[TEST 3] Testing with Sample Resume...")
try:
    with open("sample_resumes/sample_resume.txt", "r") as f:
        resume = f.read()
    with open("sample_resumes/sample_job_description.txt", "r") as f:
        job_desc = f.read()
    
    analyzer = ResumeAnalyzer()
    result = analyzer.analyze_resume(resume, job_desc)
    
    print(f"  Resume: {len(resume)} chars")
    print(f"  Job Description: {len(job_desc)} chars")
    print(f"  ATS Score: {result['ats_score']}/100")
    print(f"  Keywords Found: {len(result['matched_keywords'])}")
    print("  [OK] Sample analysis successful")
except Exception as e:
    print(f"  [FAIL] Sample analysis failed: {e}")
    sys.exit(1)

# Test 4: API endpoint simulation (without network)
print("[TEST 4] Testing API Endpoint Logic...")
try:
    from backend.api.routes import get_analyzer
    from backend.models.schemas import ATSAnalysisResponse
    
    # Get the analyzer instance
    test_analyzer = get_analyzer()
    
    # Simulate what the API does
    test_data = {
        "job_description": "Python Developer with Django experience",
        "resume_text": "John Doe - Senior Python Engineer with 10 years Django experience"
    }
    
    result = test_analyzer.analyze_resume(
        test_data["resume_text"],
        test_data["job_description"]
    )
    
    # Validate response schema
    response = ATSAnalysisResponse(**result)
    
    print(f"  ATS Score: {response.ats_score}")
    print(f"  Match Rate: {response.keyword_match_rate:.1f}%")
    print("  [OK] API endpoint logic working")
except Exception as e:
    print(f"  [FAIL] API test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*80)
print("ALL TESTS PASSED - SYSTEM IS OPERATIONAL")
print("="*80)

print("\nNEXT STEPS:")
print("1. Ensure both services are running:")
print("   - Backend API: python start_backend.py")
print("   - Frontend: npm run dev (in frontend/ directory)")
print("")
print("2. Visit the application in your browser:")
print("   - http://localhost:3000")
print("")
print("3. The frontend will automatically proxy API calls to:")
print("   - http://localhost:8000/api/analyze")
print("")
print("="*80 + "\n")
