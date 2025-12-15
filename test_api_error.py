#!/usr/bin/env python3
"""Test API and capture actual error"""
import warnings
warnings.filterwarnings('ignore')

import requests
import json
import time

time.sleep(3)

# Minimal test data
data = {
    "job_description": "Senior Developer Position",
    "resume_text": "John Doe - Python Developer with 5 years experience"
}

print("Testing API /api/analyze endpoint...")
print(f"Sending: {json.dumps(data, indent=2)}")

try:
    response = requests.post(
        "http://127.0.0.1:8000/api/analyze",
        data=data,
        timeout=60
    )
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"\nResponse Body:")
    print(response.text)
    
    if response.status_code == 200:
        print("\n✓ SUCCESS")
    else:
        print(f"\n✗ ERROR: Status {response.status_code}")
        
except Exception as e:
    print(f"\n✗ CONNECTION ERROR: {e}")
    import traceback
    traceback.print_exc()
