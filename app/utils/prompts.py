"""
Prompt templates for contract obligation extraction.
Designed for legal domain expertise and consistent output.
"""

OBLIGATION_EXTRACTION_PROMPT = """
You are a legal AI assistant specializing in contract analysis and obligation extraction. Your task is to identify and extract contractual obligations from the provided contract text.

Given the contract text below, identify and extract ALL contractual obligations, including:

1. **Specific obligations** - What needs to be done - Limit to 5 obligations
2. **Responsible parties** - Who is responsible (Party A, Party B, Company, Vendor, etc.)
3. **Due dates** - When obligations are due (specific dates, timeframes, or "Ongoing")
4. **Risk levels** - Assess risk as Low, Medium, or High based on:
   - Low: Standard obligations, minimal consequences
   - Medium: Important obligations with moderate consequences
   - High: Critical obligations with significant legal/financial consequences
5. **Plain English summary** - One-line description in simple terms

IMPORTANT GUIDELINES:
- Extract ALL obligations, not just the most obvious ones
- Be thorough in identifying both explicit and implicit obligations
- Use "Ongoing" for continuous obligations without specific end dates
- Identify parties clearly (Party A, Party B, Company, Vendor, etc.)
- Assess risk based on potential consequences and importance
- Provide clear, actionable summaries

Respond ONLY in the following JSON format:
[
  {{
    "obligation": "Specific obligation text from contract",
    "responsibleParty": "Party A/Party B/Company/Vendor/etc.",
    "dueDate": "YYYY-MM-DD or timeframe or 'Ongoing'",
    "riskLevel": "Low/Medium/High",
    "summary": "One-line plain English description"
  }}
]

Contract Text:
\"\"\"
{contract_text}
\"\"\"

Extract all obligations and respond with valid JSON only.
"""

RISK_ASSESSMENT_GUIDELINES = """
Risk Level Assessment Guidelines:

LOW RISK:
- Standard operational obligations
- Routine reporting requirements
- Minor administrative tasks
- Non-critical deadlines
- Minimal financial/legal consequences

MEDIUM RISK:
- Important business obligations
- Regulatory compliance requirements
- Moderate financial implications
- Reputation-related obligations
- Intermediate deadlines

HIGH RISK:
- Critical business obligations
- Major financial commitments
- Legal compliance requirements
- Termination triggers
- Significant penalties/consequences
- Core business functions
"""

# Fallback prompt for simpler extraction if the main prompt fails
SIMPLE_EXTRACTION_PROMPT = """
Extract contractual obligations from this contract text. For each obligation, identify:
1. What needs to be done
2. Who is responsible
3. When it's due
4. Risk level (Low/Medium/High)

Format as JSON:
[
  {{
    "obligation": "description",
    "responsibleParty": "party name",
    "dueDate": "date or Ongoing",
    "riskLevel": "Low/Medium/High",
    "summary": "brief description"
  }}
]

Contract: {contract_text}
""" 