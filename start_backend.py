#!/usr/bin/env python3
"""Start backend API on 0.0.0.0:8000 for network access"""
import warnings
warnings.filterwarnings('ignore', message='.*Numpy.*')

from backend.main import app
import uvicorn

print("=" * 80)
print("Starting AI Resume ATS Checker API Server")
print("Listening on http://0.0.0.0:8000")
print("=" * 80)

uvicorn.run(
    app,
    host="0.0.0.0",  # Listen on all interfaces
    port=8000,
    log_level="info"
)
