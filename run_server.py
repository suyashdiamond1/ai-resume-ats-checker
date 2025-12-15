#!/usr/bin/env python3
"""Wrapper to suppress numpy warnings and start the FastAPI server"""
import warnings
import os

# Suppress numpy warnings
warnings.filterwarnings('ignore', category=RuntimeWarning)
warnings.filterwarnings('ignore', message='.*Numpy built with MINGW-W64.*')

# Start the server
if __name__ == "__main__":
    import uvicorn
    from backend.main import app
    
    print("Starting FastAPI server on http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
