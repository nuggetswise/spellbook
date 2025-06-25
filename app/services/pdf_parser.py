"""
PDF parsing service for contract text extraction.
Uses PyMuPDF as primary parser with pdfminer as fallback.
"""

import fitz  # PyMuPDF
import io
from typing import Optional, Tuple
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
import logging

logger = logging.getLogger(__name__)

class PDFParser:
    """PDF text extraction service with multiple parsing strategies."""
    
    def __init__(self):
        self.primary_parser = "PyMuPDF"
        self.fallback_parser = "pdfminer"
    
    def extract_text(self, pdf_content: bytes) -> Tuple[str, str]:
        """
        Extract text from PDF content using multiple parsing strategies.
        
        Args:
            pdf_content: Raw PDF bytes
            
        Returns:
            Tuple of (extracted_text, parser_used)
        """
        # Try primary parser (PyMuPDF)
        try:
            text = self._extract_with_pymupdf(pdf_content)
            if text and len(text.strip()) > 100:
                return text, self.primary_parser
        except Exception as e:
            logger.warning(f"PyMuPDF extraction failed: {e}")
        
        # Try fallback parser (pdfminer)
        try:
            text = self._extract_with_pdfminer(pdf_content)
            if text and len(text.strip()) > 100:
                return text, self.fallback_parser
        except Exception as e:
            logger.warning(f"pdfminer extraction failed: {e}")
        
        # If both fail, return error
        raise ValueError("Failed to extract text from PDF with both parsers")
    
    def _extract_with_pymupdf(self, pdf_content: bytes) -> str:
        """
        Extract text using PyMuPDF (fitz).
        
        Args:
            pdf_content: Raw PDF bytes
            
        Returns:
            Extracted text
        """
        try:
            # Open PDF from bytes
            pdf_document = fitz.open(stream=pdf_content, filetype="pdf")
            
            text_parts = []
            
            # Extract text from each page
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                
                # Get text with layout preservation
                text = page.get_text("text")
                text_parts.append(text)
            
            pdf_document.close()
            
            # Combine all text
            full_text = "\n".join(text_parts)
            
            # Clean up the text
            cleaned_text = self._clean_extracted_text(full_text)
            
            return cleaned_text
            
        except Exception as e:
            logger.error(f"PyMuPDF extraction error: {e}")
            raise
    
    def _extract_with_pdfminer(self, pdf_content: bytes) -> str:
        """
        Extract text using pdfminer.
        
        Args:
            pdf_content: Raw PDF bytes
            
        Returns:
            Extracted text
        """
        try:
            # Create a file-like object from bytes
            pdf_stream = io.BytesIO(pdf_content)
            
            # Extract text to string
            output = io.StringIO()
            
            # Configure layout parameters for better text extraction
            laparams = LAParams(
                line_margin=0.5,
                word_margin=0.1,
                char_margin=2.0,
                boxes_flow=0.5,
                detect_vertical=True
            )
            
            extract_text_to_fp(pdf_stream, output, laparams=laparams)
            
            # Get extracted text
            text = output.getvalue()
            output.close()
            
            # Clean up the text
            cleaned_text = self._clean_extracted_text(text)
            
            return cleaned_text
            
        except Exception as e:
            logger.error(f"pdfminer extraction error: {e}")
            raise
    
    def _clean_extracted_text(self, text: str) -> str:
        """
        Clean and normalize extracted text.
        
        Args:
            text: Raw extracted text
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove excessive whitespace
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Remove excessive spaces
            line = ' '.join(line.split())
            
            # Skip empty lines
            if line.strip():
                cleaned_lines.append(line)
        
        # Join lines with proper spacing
        cleaned_text = '\n'.join(cleaned_lines)
        
        # Remove common PDF artifacts
        cleaned_text = self._remove_pdf_artifacts(cleaned_text)
        
        return cleaned_text
    
    def _remove_pdf_artifacts(self, text: str) -> str:
        """
        Remove common PDF extraction artifacts.
        
        Args:
            text: Text to clean
            
        Returns:
            Cleaned text
        """
        import re
        
        # Remove page numbers and headers/footers
        text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)
        
        # Remove common PDF artifacts
        artifacts = [
            r'Page \d+ of \d+',
            r'Confidential',
            r'Draft',
            r'Final',
            r'Copy',
            r'Original',
        ]
        
        for artifact in artifacts:
            text = re.sub(artifact, '', text, flags=re.IGNORECASE)
        
        # Remove excessive line breaks
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text.strip()
    
    def get_pdf_info(self, pdf_content: bytes) -> dict:
        """
        Get basic information about the PDF.
        
        Args:
            pdf_content: Raw PDF bytes
            
        Returns:
            Dictionary with PDF information
        """
        try:
            pdf_document = fitz.open(stream=pdf_content, filetype="pdf")
            
            info = {
                "page_count": len(pdf_document),
                "file_size": len(pdf_content),
                "metadata": pdf_document.metadata
            }
            
            pdf_document.close()
            return info
            
        except Exception as e:
            logger.error(f"Error getting PDF info: {e}")
            return {
                "page_count": 0,
                "file_size": len(pdf_content),
                "metadata": {}
            } 