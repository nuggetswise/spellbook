"""
Validation utilities for contract obligation extraction.
Ensures data quality and handles edge cases.
"""

import json
import re
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, validator

class Obligation(BaseModel):
    """Data model for extracted obligations."""
    obligation: str
    responsibleParty: str
    dueDate: str
    riskLevel: str
    summary: str
    
    @validator('riskLevel')
    def validate_risk_level(cls, v):
        valid_levels = ['Low', 'Medium', 'High']
        if v not in valid_levels:
            raise ValueError(f'Risk level must be one of {valid_levels}')
        return v
    
    @validator('dueDate')
    def validate_due_date(cls, v):
        if v.lower() == 'ongoing':
            return 'Ongoing'
        
        # Try to parse date formats
        date_patterns = [
            r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
            r'\d{1,2}/\d{1,2}/\d{4}',  # MM/DD/YYYY
            r'\d{1,2}-\d{1,2}-\d{4}',  # MM-DD-YYYY
        ]
        
        for pattern in date_patterns:
            if re.match(pattern, v):
                return v
        
        # If not a recognized date format, return as is
        return v

def validate_json_response(response_text: str) -> Optional[List[Dict[str, Any]]]:
    """
    Validate and parse JSON response from LLM.
    
    Args:
        response_text: Raw response from LLM
        
    Returns:
        Parsed obligations list or None if invalid
    """
    try:
        # Clean the response text
        cleaned_text = clean_json_response(response_text)
        
        # Parse JSON
        obligations = json.loads(cleaned_text)
        
        # Validate structure
        if not isinstance(obligations, list):
            return None
            
        # Validate each obligation
        validated_obligations = []
        for obligation in obligations:
            try:
                validated_obligation = Obligation(**obligation)
                validated_obligations.append(validated_obligation.dict())
            except Exception as e:
                print(f"Invalid obligation format: {e}")
                continue
                
        return validated_obligations if validated_obligations else None
        
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        return None
    except Exception as e:
        print(f"Validation error: {e}")
        return None

def clean_json_response(response_text: str) -> str:
    """
    Clean LLM response to extract valid JSON.
    
    Args:
        response_text: Raw LLM response
        
    Returns:
        Cleaned JSON string
    """
    # Remove markdown code blocks
    response_text = re.sub(r'```json\s*', '', response_text)
    response_text = re.sub(r'```\s*', '', response_text)
    
    # Remove leading/trailing whitespace
    response_text = response_text.strip()
    
    # Find JSON array start and end
    start_idx = response_text.find('[')
    end_idx = response_text.rfind(']')
    
    if start_idx != -1 and end_idx != -1:
        return response_text[start_idx:end_idx + 1]
    
    return response_text

def validate_contract_text(text: str) -> bool:
    """
    Validate that contract text is suitable for processing.
    
    Args:
        text: Contract text to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not text or len(text.strip()) < 50:
        return False
    
    # Check for minimum meaningful content
    words = text.split()
    if len(words) < 20:
        return False
    
    return True

def extract_dates_from_text(text: str) -> List[str]:
    """
    Extract potential dates from text for validation.
    
    Args:
        text: Text to search for dates
        
    Returns:
        List of found date strings
    """
    date_patterns = [
        r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
        r'\d{1,2}/\d{1,2}/\d{4}',  # MM/DD/YYYY
        r'\d{1,2}-\d{1,2}-\d{4}',  # MM-DD-YYYY
        r'\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}\b',  # DD Month YYYY
    ]
    
    dates = []
    for pattern in date_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        dates.extend(matches)
    
    return list(set(dates))  # Remove duplicates

def sanitize_party_name(party_name: str) -> str:
    """
    Sanitize party names for consistency.
    
    Args:
        party_name: Raw party name
        
    Returns:
        Sanitized party name
    """
    # Common party name variations
    party_mappings = {
        'party a': 'Party A',
        'party b': 'Party B',
        'company': 'Company',
        'vendor': 'Vendor',
        'client': 'Client',
        'customer': 'Customer',
        'supplier': 'Supplier',
        'contractor': 'Contractor',
        'subcontractor': 'Subcontractor',
    }
    
    normalized = party_name.strip().lower()
    return party_mappings.get(normalized, party_name.strip()) 