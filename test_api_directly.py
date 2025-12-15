#!/usr/bin/env python3
"""
Test the API endpoint directly by making HTTP requests
Only run this after starting the backend with: python start_backend.py

Usage:
1. Start backend in one terminal: python start_backend.py
2. Run this script in another terminal: python test_api_directly.py
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """Test if backend is running"""
    print("\n[TEST 1] Checking if backend is running...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        print(f"  Status: {response.status_code}")
        print(f"  Response: {response.json()}")
        return True
    except requests.exceptions.ConnectionError:
        print("  ERROR: Cannot connect to backend on port 8000")
        print("  Make sure to run: python start_backend.py")
        return False
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

def test_analyze():
    """Test the analyze endpoint"""
    print("\n[TEST 2] Testing /api/analyze endpoint...")
    
    payload = {
        "job_description": "Senior Python Developer with 5+ years Django experience, AWS expertise, and PostgreSQL knowledge",
        "resume_text": """
        John Doe
        Senior Software Engineer
        
        SKILLS
        - Python (Django, FastAPI, Flask)
        - AWS (EC2, S3, RDS)
        - PostgreSQL, Redis
        - Docker, Kubernetes
        
        EXPERIENCE
        Senior Python Developer at TechCorp (2020-2024)
        - Built scalable APIs using Django and FastAPI
        - Managed AWS infrastructure
        - Optimized PostgreSQL queries
        
        Python Developer at StartupXYZ (2018-2020)
        - Full-stack Django development
        - Database optimization
        
        EDUCATION
        BS Computer Science - State University (2018)
        """
    }
    
    try:
        print(f"  Sending request to {BASE_URL}/api/analyze")
        print(f"  Job Description: {payload['job_description'][:60]}...")
        print(f"  Resume: {len(payload['resume_text'])} characters")
        
        response = requests.post(
            f"{BASE_URL}/api/analyze",
            json=payload,
            timeout=30
        )
        
        print(f"  Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n  SUCCESS! API Response:")
            print(f"    ATS Score: {data['ats_score']}/100")
            print(f"    Keyword Match Rate: {data['keyword_match_rate']:.1f}%")
            print(f"    Matched Keywords: {len(data['matched_keywords'])}")
            print(f"    Missing Keywords: {len(data['missing_keywords'])}")
            print(f"    Suggestions: {len(data['suggestions'])}")
            
            print("\n  Matched Keywords:")
            for kw in data['matched_keywords'][:10]:
                print(f"    - {kw}")
            if len(data['matched_keywords']) > 10:
                print(f"    ... and {len(data['matched_keywords']) - 10} more")
            
            print("\n  Top Suggestions:")
            for i, suggestion in enumerate(data['suggestions'][:5], 1):
                print(f"    {i}. {suggestion}")
            
            return True
        else:
            print(f"  ERROR: Got status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("  ERROR: Request timed out (>30 seconds)")
        print("  This might happen if the backend is still initializing")
        return False
    except requests.exceptions.ConnectionError:
        print("  ERROR: Cannot connect to backend")
        print("  Make sure to run: python start_backend.py")
        return False
    except Exception as e:
        print(f"  ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("="*80)
    print("AI RESUME ATS CHECKER - API DIRECT TEST")
    print("="*80)
    print("\nNote: Make sure backend is running!")
    print("In another terminal, run: python start_backend.py")
    print("\nWaiting 2 seconds for user to read this...")
    time.sleep(2)
    
    # Test health check first
    if not test_health():
        print("\n" + "="*80)
        print("BACKEND NOT RUNNING - Please start it first!")
        print("="*80)
        exit(1)
    
    # Test analyze endpoint
    if test_analyze():
        print("\n" + "="*80)
        print("ALL TESTS PASSED!")
        print("="*80)
        print("\nYour API is working correctly!")
        print("Frontend should now be able to communicate with the backend.")
        print("\nVisit: http://localhost:3000 to use the web interface")
        exit(0)
    else:
        print("\n" + "="*80)
        print("TEST FAILED")
        print("="*80)
        exit(1)
