"""
Core obligation extraction service.
Orchestrates the entire process from file upload to obligation extraction.
"""

import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent.parent
sys.path.insert(0, str(parent_dir))

import logging
from typing import List, Dict, Any, Optional, Tuple
from app.services.pdf_parser import PDFParser
from app.services.llm_service import LLMService
from app.utils.validators import validate_contract_text, sanitize_party_name
from app.config.settings import settings

logger = logging.getLogger(__name__)

class ObligationExtractor:
    """Main service for extracting obligations from contracts."""
    
    def __init__(self):
        self.pdf_parser = PDFParser()
        self.llm_service = LLMService()
    
    def process_contract(self, file_content: bytes, file_type: str) -> Dict[str, Any]:
        """
        Process a contract file and extract obligations.
        
        Args:
            file_content: Raw file content
            file_type: Type of file ('pdf' or 'txt')
            
        Returns:
            Dictionary with extraction results
        """
        try:
            # Extract text from file
            contract_text, parser_used = self._extract_text(file_content, file_type)
            
            # Validate contract text
            if not validate_contract_text(contract_text):
                raise ValueError("Contract text is too short or invalid")
            
            # Extract obligations using LLM
            obligations, api_used = self.llm_service.extract_obligations(contract_text)
            
            # Post-process obligations
            processed_obligations = self._post_process_obligations(obligations)
            
            # Prepare results
            results = {
                "success": True,
                "obligations": processed_obligations,
                "total_obligations": len(processed_obligations),
                "api_used": api_used,
                "parser_used": parser_used,
                "contract_length": len(contract_text),
                "risk_summary": self._generate_risk_summary(processed_obligations)
            }
            
            logger.info(f"Successfully extracted {len(processed_obligations)} obligations using {api_used}")
            return results
            
        except Exception as e:
            logger.error(f"Error processing contract: {e}")
            return {
                "success": False,
                "error": str(e),
                "obligations": [],
                "total_obligations": 0
            }
    
    def _extract_text(self, file_content: bytes, file_type: str) -> Tuple[str, str]:
        """
        Extract text from file based on type.
        
        Args:
            file_content: Raw file content
            file_type: Type of file
            
        Returns:
            Tuple of (extracted_text, parser_used)
        """
        if file_type.lower() == 'pdf':
            return self.pdf_parser.extract_text(file_content)
        elif file_type.lower() == 'txt':
            # For text files, decode bytes to string
            text = file_content.decode('utf-8', errors='ignore')
            return text, "text_decoder"
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    
    def _post_process_obligations(self, obligations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Post-process extracted obligations for consistency and quality.
        
        Args:
            obligations: Raw obligations from LLM
            
        Returns:
            Processed obligations
        """
        processed_obligations = []
        
        for obligation in obligations:
            try:
                # Sanitize party names
                obligation['responsibleParty'] = sanitize_party_name(obligation['responsibleParty'])
                
                # Clean obligation text
                obligation['obligation'] = self._clean_obligation_text(obligation['obligation'])
                
                # Clean summary
                obligation['summary'] = self._clean_summary_text(obligation['summary'])
                
                # Add confidence score (placeholder for now)
                obligation['confidence'] = 0.85
                
                processed_obligations.append(obligation)
                
            except Exception as e:
                logger.warning(f"Error processing obligation: {e}")
                continue
        
        return processed_obligations
    
    def _clean_obligation_text(self, text: str) -> str:
        """
        Clean obligation text for consistency.
        
        Args:
            text: Raw obligation text
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = ' '.join(text.split())
        
        # Remove common artifacts
        text = text.replace('"', '').replace('"', '').replace('"', '')
        text = text.replace(''', "'").replace(''', "'")
        
        return text.strip()
    
    def _clean_summary_text(self, text: str) -> str:
        """
        Clean summary text for consistency.
        
        Args:
            text: Raw summary text
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = ' '.join(text.split())
        
        # Ensure it ends with a period
        if text and not text.endswith('.'):
            text += '.'
        
        return text.strip()
    
    def _generate_risk_summary(self, obligations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate risk summary from obligations.
        
        Args:
            obligations: List of obligations
            
        Returns:
            Risk summary dictionary
        """
        risk_counts = {"Low": 0, "Medium": 0, "High": 0}
        
        for obligation in obligations:
            risk_level = obligation.get('riskLevel', 'Medium')
            if risk_level in risk_counts:
                risk_counts[risk_level] += 1
        
        total = len(obligations)
        
        return {
            "total_obligations": total,
            "risk_breakdown": risk_counts,
            "high_risk_percentage": (risk_counts["High"] / total * 100) if total > 0 else 0,
            "medium_risk_percentage": (risk_counts["Medium"] / total * 100) if total > 0 else 0,
            "low_risk_percentage": (risk_counts["Low"] / total * 100) if total > 0 else 0
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Get system status including API availability.
        
        Returns:
            System status dictionary
        """
        api_status = self.llm_service.get_api_status()
        
        return {
            "apis_available": api_status,
            "pdf_parser_available": True,  # Always available
            "system_ready": api_status["any_available"]
        }
    
    def test_extraction(self, sample_text: str) -> Dict[str, Any]:
        """
        Test obligation extraction with sample text.
        
        Args:
            sample_text: Sample contract text for testing
            
        Returns:
            Test results
        """
        try:
            obligations, api_used = self.llm_service.extract_obligations(sample_text)
            
            return {
                "success": True,
                "obligations_found": len(obligations),
                "api_used": api_used,
                "sample_obligations": obligations[:3]  # First 3 for preview
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            } 