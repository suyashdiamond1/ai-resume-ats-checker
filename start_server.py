#!/usr/bin/env python3
"""Run the FastAPI server"""
import warnings
warnings.filterwarnings('ignore', message='.*Numpy.*')

from backend.main import app
import uvicorn

print("=" * 80, flush=True)
print("Starting AI Resume ATS Checker API Server", flush=True)
print("=" * 80, flush=True)

uvicorn.run(
    app,
    host="127.0.0.1",
    port=8000,
    log_level="info"
)
