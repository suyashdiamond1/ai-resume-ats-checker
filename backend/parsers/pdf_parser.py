"""PDF Resume Parser"""
import io
from typing import Union
import pdfplumber


class PDFParser:
    """Parse PDF files and extract text content"""
    
    @staticmethod
    def extract_text(file_content: Union[bytes, io.BytesIO]) -> str:
        """
        Extract text from PDF file
        
        Args:
            file_content: PDF file as bytes or BytesIO object
            
        Returns:
            Extracted text as string
        """
        if isinstance(file_content, bytes):
            file_content = io.BytesIO(file_content)
        
        text = ""
        try:
            with pdfplumber.open(file_content) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            raise ValueError(f"Error parsing PDF: {str(e)}")
        
        return text.strip()
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean and normalize extracted text
        
        Args:
            text: Raw extracted text
            
        Returns:
            Cleaned text
        """
        # Remove extra whitespace
        text = " ".join(text.split())
        # Remove special characters but keep important punctuation
        text = text.replace("\t", " ").replace("\r", " ")
        return text.strip()
