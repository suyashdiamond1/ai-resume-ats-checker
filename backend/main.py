"""
AI Resume ATS Checker - Main FastAPI Application
"""
import sys
from pathlib import Path

# Add backend directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from api.routes import router

app = FastAPI(
    title="AI Resume ATS Checker",
    description="Analyze resume ATS compatibility against job descriptions",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api", tags=["ATS Analysis"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Resume ATS Checker API",
        "version": "1.0.0",
        "endpoints": {
            "analyze": "/api/analyze",
            "analyze-json": "/api/analyze-json",
            "health": "/api/health",
            "docs": "/docs"
        }
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
