"""Resume Analysis Service"""
import io
from typing import Union, Dict
from parsers import PDFParser, DOCXParser, TextParser
from .ats_scorer import ATSScorer


class ResumeAnalyzer:
    """Main service for analyzing resumes"""
    
    def __init__(self):
        """Initialize the analyzer"""
        self.pdf_parser = PDFParser()
        self.docx_parser = DOCXParser()
        self.text_parser = TextParser()
        self.ats_scorer = ATSScorer()
    
    def parse_resume(self, file_content: Union[bytes, str], file_type: str) -> str:
        """
        Parse resume from different file formats
        
        Args:
            file_content: File content as bytes or string
            file_type: File type ('pdf', 'docx', 'text')
            
        Returns:
            Extracted and cleaned text
        """
        file_type = file_type.lower()
        
        if file_type == 'pdf':
            text = self.pdf_parser.extract_text(file_content)
            return self.pdf_parser.clean_text(text)
        
        elif file_type in ['docx', 'doc']:
            text = self.docx_parser.extract_text(file_content)
            return self.docx_parser.clean_text(text)
        
        elif file_type in ['txt', 'text']:
            if isinstance(file_content, bytes):
                file_content = file_content.decode('utf-8')
            text = self.text_parser.extract_text(file_content)
            return self.text_parser.clean_text(text)
        
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    
    def analyze_resume(
        self, 
        resume_text: str, 
        job_description: str
    ) -> Dict:
        """
        Analyze resume against job description
        
        Args:
            resume_text: Cleaned resume text
            job_description: Job description text
            
        Returns:
            ATS analysis results
        """
        if not resume_text or len(resume_text.strip()) < 50:
            raise ValueError("Resume text is too short or empty")
        
        if not job_description or len(job_description.strip()) < 20:
            raise ValueError("Job description is too short or empty")
        
        return self.ats_scorer.analyze(resume_text, job_description)
