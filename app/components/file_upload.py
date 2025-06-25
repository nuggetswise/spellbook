"""
File upload component for contract documents.
Supports PDF and text file uploads with validation.
"""

import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent.parent
sys.path.insert(0, str(parent_dir))

import streamlit as st
from typing import Optional, Tuple
import io
from app.config.settings import settings

def render_file_upload() -> Optional[Tuple[bytes, str]]:
    """
    Render file upload component.
    
    Returns:
        Tuple of (file_content, file_type) if file uploaded, None otherwise
    """
    st.header("📄 Upload Contract")
    
    # File upload section
    uploaded_file = st.file_uploader(
        "Choose a contract file",
        type=['pdf', 'txt'],
        help="Upload a PDF or text file containing your contract"
    )
    
    if uploaded_file is not None:
        # Validate file size
        if uploaded_file.size > settings.MAX_FILE_SIZE:
            st.error(f"File too large. Maximum size is {settings.MAX_FILE_SIZE // (1024*1024)}MB")
            return None
        
        # Get file content
        file_content = uploaded_file.read()
        file_type = uploaded_file.name.split('.')[-1].lower()
        
        # Display file info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("File Size", f"{uploaded_file.size // 1024} KB")
        with col2:
            st.metric("File Type", file_type.upper())
        with col3:
            st.metric("File Name", uploaded_file.name[:20] + "..." if len(uploaded_file.name) > 20 else uploaded_file.name)
        
        # Show preview for text files
        if file_type == 'txt':
            with st.expander("📖 Text Preview"):
                try:
                    text_preview = file_content.decode('utf-8', errors='ignore')[:500]
                    st.text_area("Preview (first 500 characters):", text_preview, height=200)
                except Exception as e:
                    st.error(f"Error reading text file: {e}")
                    return None
        
        # Show PDF info for PDF files
        elif file_type == 'pdf':
            with st.expander("📋 PDF Information"):
                try:
                    from app.services.pdf_parser import PDFParser
                    pdf_parser = PDFParser()
                    pdf_info = pdf_parser.get_pdf_info(file_content)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Pages", pdf_info.get('page_count', 'Unknown'))
                    with col2:
                        st.metric("Size", f"{pdf_info.get('file_size', 0) // 1024} KB")
                    
                    # Show metadata if available
                    metadata = pdf_info.get('metadata', {})
                    if metadata:
                        st.write("**Document Metadata:**")
                        for key, value in metadata.items():
                            if value:
                                st.write(f"- **{key}:** {value}")
                
                except Exception as e:
                    st.warning(f"Could not read PDF metadata: {e}")
        
        return file_content, file_type
    
    return None

def render_demo_contract() -> Optional[str]:
    """
    Render demo contract option for testing.
    
    Returns:
        Demo contract text if selected, None otherwise
    """
    st.subheader("🧪 Try Demo Contract")
    
    demo_option = st.selectbox(
        "Choose a demo contract to test:",
        ["None", "Service Agreement", "Employment Contract", "NDA", "Custom Text"]
    )
    
    if demo_option == "Service Agreement":
        return """
        SERVICE AGREEMENT
        
        This Service Agreement (the "Agreement") is entered into on January 15, 2024, between ABC Company ("Client") and XYZ Services ("Provider").
        
        SECTION 1: SERVICES
        Provider shall deliver consulting services to Client commencing February 1, 2024, and continuing for a period of 12 months. Provider must submit monthly progress reports by the 5th of each month.
        
        SECTION 2: PAYMENT TERMS
        Client shall pay Provider $10,000 per month, due within 30 days of invoice receipt. Late payments shall incur a 2% monthly penalty.
        
        SECTION 3: CONFIDENTIALITY
        Both parties must maintain strict confidentiality of all proprietary information shared during the term of this agreement and for 3 years thereafter.
        
        SECTION 4: TERMINATION
        Either party may terminate this agreement with 30 days written notice. Provider must complete all work in progress and deliver final deliverables within 14 days of termination.
        
        SECTION 5: COMPLIANCE
        Provider must comply with all applicable laws and regulations, including data protection requirements. Provider shall obtain necessary permits and licenses at their own expense.
        """
    
    elif demo_option == "Employment Contract":
        return """
        EMPLOYMENT AGREEMENT
        
        This Employment Agreement is made between TechCorp Inc. ("Employer") and John Smith ("Employee") effective March 1, 2024.
        
        SECTION 1: POSITION AND DUTIES
        Employee shall serve as Senior Software Engineer and report to the CTO. Employee must work 40 hours per week and attend all mandatory meetings.
        
        SECTION 2: COMPENSATION
        Employer shall pay Employee an annual salary of $120,000, payable bi-weekly. Employee is eligible for annual performance bonuses up to 20% of base salary.
        
        SECTION 3: BENEFITS
        Employee shall receive health insurance, 401(k) matching, and 20 days of paid time off annually. Employee must submit PTO requests at least 2 weeks in advance.
        
        SECTION 4: INTELLECTUAL PROPERTY
        Employee must assign all inventions and intellectual property created during employment to Employer. Employee shall sign all necessary documents to perfect such assignments.
        
        SECTION 5: NON-COMPETE
        Employee shall not work for competitors or solicit Employer's clients for 12 months after termination. Employee must return all company property within 7 days of termination.
        """
    
    elif demo_option == "NDA":
        return """
        NON-DISCLOSURE AGREEMENT
        
        This Non-Disclosure Agreement is entered into between StartupXYZ ("Disclosing Party") and InvestorABC ("Receiving Party") on April 10, 2024.
        
        SECTION 1: CONFIDENTIAL INFORMATION
        Receiving Party shall maintain strict confidentiality of all proprietary information, trade secrets, and business plans disclosed by Disclosing Party.
        
        SECTION 2: USE RESTRICTIONS
        Receiving Party may only use confidential information for evaluation purposes and must not disclose it to any third parties without prior written consent.
        
        SECTION 3: SECURITY MEASURES
        Receiving Party must implement reasonable security measures to protect confidential information and limit access to authorized personnel only.
        
        SECTION 4: RETURN OF MATERIALS
        Upon request or termination of discussions, Receiving Party must return or destroy all confidential materials within 10 business days.
        
        SECTION 5: DURATION
        This agreement remains in effect for 5 years from the date of disclosure, regardless of whether a business relationship is established.
        """
    
    elif demo_option == "Custom Text":
        custom_text = st.text_area(
            "Enter your own contract text:",
            height=300,
            placeholder="Paste your contract text here..."
        )
        if custom_text.strip():
            return custom_text
    
    return None 