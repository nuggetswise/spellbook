"""
LLM service for contract obligation extraction.
Supports OpenAI GPT-4 and Google Gemini with automatic fallback.
"""

import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent.parent
sys.path.insert(0, str(parent_dir))

import openai
import google.generativeai as genai
import logging
from typing import List, Dict, Any, Optional, Tuple
from app.config.settings import settings
from app.utils.prompts import OBLIGATION_EXTRACTION_PROMPT, SIMPLE_EXTRACTION_PROMPT

logger = logging.getLogger(__name__)

class LLMService:
    """LLM service with dual API support and fallback mechanisms."""
    
    def __init__(self):
        self.openai_client = None
        self.gemini_model = None
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize LLM clients based on available API keys."""
        # Initialize OpenAI client
        if settings.OPENAI_API_KEY:
            try:
                self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
                logger.info("OpenAI client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {e}")
        
        # Initialize Gemini client
        if settings.GEMINI_API_KEY:
            try:
                genai.configure(api_key=settings.GEMINI_API_KEY)
                self.gemini_model = genai.GenerativeModel(settings.GEMINI_MODEL)
                logger.info("Gemini client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini client: {e}")
    
    def extract_obligations(self, contract_text: str) -> Tuple[List[Dict[str, Any]], str]:
        """
        Extract obligations from contract text using available LLM APIs.
        
        Args:
            contract_text: Contract text to analyze
            
        Returns:
            Tuple of (obligations_list, api_used)
        """
        # Try OpenAI first (preferred for legal text)
        if self.openai_client:
            try:
                obligations = self._extract_with_openai(contract_text)
                if obligations:
                    return obligations, "OpenAI GPT-4"
            except Exception as e:
                logger.warning(f"OpenAI extraction failed: {e}")
        
        # Try Gemini as fallback
        if self.gemini_model:
            try:
                obligations = self._extract_with_gemini(contract_text)
                if obligations:
                    return obligations, "Google Gemini"
            except Exception as e:
                logger.warning(f"Gemini extraction failed: {e}")
        
        # If both fail, raise error
        raise Exception("All LLM APIs failed to extract obligations")
    
    def _extract_with_openai(self, contract_text: str) -> Optional[List[Dict[str, Any]]]:
        """
        Extract obligations using OpenAI GPT-4.
        
        Args:
            contract_text: Contract text to analyze
            
        Returns:
            List of obligations or None if failed
        """
        try:
            # Prepare the prompt
            prompt = OBLIGATION_EXTRACTION_PROMPT.format(contract_text=contract_text)
            
            # Make API call using new OpenAI API format
            response = self.openai_client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a legal AI assistant specializing in contract analysis."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=settings.MAX_TOKENS,
                temperature=settings.TEMPERATURE
            )
            
            # Extract response content
            response_text = response.choices[0].message.content
            
            # Parse and validate response
            from app.utils.validators import validate_json_response
            obligations = validate_json_response(response_text)
            
            return obligations
            
        except Exception as e:
            logger.error(f"OpenAI extraction error: {e}")
            raise
    
    def _extract_with_gemini(self, contract_text: str) -> Optional[List[Dict[str, Any]]]:
        """
        Extract obligations using Google Gemini.
        
        Args:
            contract_text: Contract text to analyze
            
        Returns:
            List of obligations or None if failed
        """
        try:
            # Prepare the prompt
            prompt = OBLIGATION_EXTRACTION_PROMPT.format(contract_text=contract_text)
            
            # Make API call
            response = self.gemini_model.generate_content(prompt)
            
            # Extract response content
            response_text = response.text
            
            # Parse and validate response
            from app.utils.validators import validate_json_response
            obligations = validate_json_response(response_text)
            
            return obligations
            
        except Exception as e:
            logger.error(f"Gemini extraction error: {e}")
            raise
    
    def _extract_with_fallback_prompt(self, contract_text: str) -> Optional[List[Dict[str, Any]]]:
        """
        Extract obligations using a simpler fallback prompt.
        
        Args:
            contract_text: Contract text to analyze
            
        Returns:
            List of obligations or None if failed
        """
        try:
            # Use simpler prompt
            prompt = SIMPLE_EXTRACTION_PROMPT.format(contract_text=contract_text)
            
            # Try with available APIs
            if self.openai_client:
                try:
                    response = self.openai_client.chat.completions.create(
                        model=settings.OPENAI_MODEL,
                        messages=[
                            {"role": "system", "content": "Extract contractual obligations in JSON format."},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=settings.MAX_TOKENS,
                        temperature=settings.TEMPERATURE
                    )
                    
                    response_text = response.choices[0].message.content
                    from app.utils.validators import validate_json_response
                    return validate_json_response(response_text)
                    
                except Exception as e:
                    logger.warning(f"OpenAI fallback failed: {e}")
            
            if self.gemini_model:
                try:
                    response = self.gemini_model.generate_content(prompt)
                    response_text = response.text
                    from app.utils.validators import validate_json_response
                    return validate_json_response(response_text)
                    
                except Exception as e:
                    logger.warning(f"Gemini fallback failed: {e}")
            
            return None
            
        except Exception as e:
            logger.error(f"Fallback extraction error: {e}")
            return None
    
    def get_api_status(self) -> Dict[str, bool]:
        """
        Get status of available APIs.
        
        Returns:
            Dictionary with API availability status
        """
        return {
            "openai_available": self.openai_client is not None,
            "gemini_available": self.gemini_model is not None,
            "any_available": self.openai_client is not None or self.gemini_model is not None
        }
    
    def test_api_connection(self) -> Dict[str, bool]:
        """
        Test connection to available APIs.
        
        Returns:
            Dictionary with API connection test results
        """
        results = {}
        
        # Test OpenAI
        if self.openai_client:
            try:
                response = self.openai_client.chat.completions.create(
                    model=settings.OPENAI_MODEL,
                    messages=[{"role": "user", "content": "Test"}],
                    max_tokens=10
                )
                results["openai_working"] = True
            except Exception as e:
                logger.error(f"OpenAI test failed: {e}")
                results["openai_working"] = False
        else:
            results["openai_working"] = False
        
        # Test Gemini
        if self.gemini_model:
            try:
                response = self.gemini_model.generate_content("Test")
                results["gemini_working"] = True
            except Exception as e:
                logger.error(f"Gemini test failed: {e}")
                results["gemini_working"] = False
        else:
            results["gemini_working"] = False
        
        return results 