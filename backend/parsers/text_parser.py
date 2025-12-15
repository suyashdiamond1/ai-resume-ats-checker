"""Plain Text Parser"""


class TextParser:
    """Parse plain text content"""
    
    @staticmethod
    def extract_text(text: str) -> str:
        """
        Extract and clean plain text
        
        Args:
            text: Plain text string
            
        Returns:
            Cleaned text
        """
        return text.strip()
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean and normalize text
        
        Args:
            text: Raw text
            
        Returns:
            Cleaned text
        """
        # Remove extra whitespace
        text = " ".join(text.split())
        # Remove special characters but keep important punctuation
        text = text.replace("\t", " ").replace("\r", " ")
        return text.strip()
