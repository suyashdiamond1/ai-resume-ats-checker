"""Data models for API requests and responses"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class SectionAnalysis(BaseModel):
    """Analysis of resume sections"""
    skills: bool = Field(..., description="Whether skills section is present")
    experience: bool = Field(..., description="Whether experience section is present")
    education: bool = Field(..., description="Whether education section is present")


class ATSAnalysisResponse(BaseModel):
    """ATS Analysis Response"""
    ats_score: int = Field(..., ge=0, le=100, description="ATS compatibility score (0-100)")
    matched_keywords: List[str] = Field(..., description="Keywords found in resume matching job description")
    missing_keywords: List[str] = Field(..., description="Important keywords missing from resume")
    section_analysis: SectionAnalysis = Field(..., description="Resume section analysis")
    suggestions: List[str] = Field(..., description="Improvement suggestions")
    keyword_match_rate: float = Field(..., description="Percentage of job keywords found in resume")
    skill_gaps: List[str] = Field(default=[], description="Identified skill gaps")


class AnalyzeRequest(BaseModel):
    """Request model for analyze endpoint"""
    job_description: str = Field(..., min_length=10, description="Job description text")
    resume_text: Optional[str] = Field(None, description="Resume as plain text (if not uploading file)")
