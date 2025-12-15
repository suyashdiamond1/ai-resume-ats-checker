"""API Routes for Resume ATS Checker"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import io

from models.schemas import ATSAnalysisResponse, AnalyzeRequest
from services.resume_analyzer import ResumeAnalyzer

router = APIRouter()
_analyzer = None  # Lazy-loaded


def get_analyzer():
    """Get or create the analyzer instance (lazy loading)"""
    global _analyzer
    if _analyzer is None:
        print("Initializing ResumeAnalyzer...")
        _analyzer = ResumeAnalyzer()
        print("ResumeAnalyzer initialized successfully")
    return _analyzer


@router.post("/analyze", response_model=ATSAnalysisResponse)
async def analyze_resume(
    job_description: str = Form(..., min_length=10),
    resume_file: Optional[UploadFile] = File(None),
    resume_text: Optional[str] = Form(None)
):
    """
    Analyze resume against job description
    
    Accepts either:
    - resume_file: Uploaded PDF/DOCX file
    - resume_text: Plain text resume
    
    Args:
        job_description: Job description text (required)
        resume_file: Resume file upload (PDF or DOCX)
        resume_text: Resume as plain text
        
    Returns:
        ATS analysis results with score, keywords, and suggestions
    """
    try:
        # Validate inputs
        if not resume_file and not resume_text:
            raise HTTPException(
                status_code=400,
                detail="Either resume_file or resume_text must be provided"
            )
        
        # Parse resume
        if resume_file:
            # Read file content
            content = await resume_file.read()
            
            # Determine file type
            filename = resume_file.filename.lower()
            if filename.endswith('.pdf'):
                file_type = 'pdf'
            elif filename.endswith(('.docx', '.doc')):
                file_type = 'docx'
            elif filename.endswith('.txt'):
                file_type = 'text'
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Unsupported file format. Please upload PDF, DOCX, or TXT file."
                )
            
            # Parse the file
            try:
                parsed_resume = get_analyzer().parse_resume(content, file_type)
            except Exception as parse_error:
                print(f"Parse error: {str(parse_error)}")
                raise HTTPException(
                    status_code=400,
                    detail=f"Failed to parse resume: {str(parse_error)}"
                )
        else:
            # Use plain text
            parsed_resume = resume_text
        
        # Validate parsed content
        if not parsed_resume or len(parsed_resume.strip()) < 50:
            raise HTTPException(
                status_code=400,
                detail="Resume content is too short or could not be extracted properly"
            )
        
        # Perform ATS analysis
        try:
            analysis_result = get_analyzer().analyze_resume(parsed_resume, job_description)
        except Exception as analysis_error:
            print(f"Analysis error: {str(analysis_error)}")
            import traceback
            traceback.print_exc()
            raise HTTPException(
                status_code=500,
                detail=f"Analysis failed: {str(analysis_error)}"
            )
        
        return ATSAnalysisResponse(**analysis_result)
    
    except HTTPException:
        raise
    except ValueError as e:
        print(f"ValueError: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/analyze-json", response_model=ATSAnalysisResponse)
async def analyze_resume_json(payload: AnalyzeRequest):
    """Analyze resume using JSON payload.

    Accepts JSON body with fields:
    - job_description: str (min_length=10)
    - resume_text: Optional[str]

    This endpoint mirrors `/api/analyze` but expects `application/json` instead of
    `multipart/form-data`.
    """
    try:
        jd = payload.job_description
        resume_text = payload.resume_text

        if not jd or len(jd.strip()) < 10:
            raise HTTPException(status_code=400, detail="Job description is too short (min 10 characters)")

        if not resume_text or len(resume_text.strip()) < 50:
            raise HTTPException(status_code=400, detail="Resume text is too short or missing (min ~50 characters)")

        try:
            analysis_result = get_analyzer().analyze_resume(resume_text, jd)
        except Exception as analysis_error:
            print(f"Analysis error (JSON): {str(analysis_error)}")
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Analysis failed: {str(analysis_error)}")

        return ATSAnalysisResponse(**analysis_result)

    except HTTPException:
        raise
    except ValueError as e:
        print(f"ValueError: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Unexpected error (JSON): {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Resume ATS Checker"}
