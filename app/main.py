"""
Main Streamlit application for Contract Obligation Extractor.
Orchestrates all components and provides the complete user interface.
"""

import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

import streamlit as st
import time
import logging
from typing import Optional, Tuple
from app.services.obligation_extractor import ObligationExtractor
from app.components.file_upload import render_file_upload, render_demo_contract
from app.components.results_table import render_obligations_table
from app.config.settings import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Contract Obligation Extractor",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main application function."""
    
    # Initialize session state
    if 'extraction_results' not in st.session_state:
        st.session_state.extraction_results = None
    if 'processing' not in st.session_state:
        st.session_state.processing = False
    
    # Header
    st.title("📋 Contract Obligation Extractor")
    
    # Enhanced hero section
    st.markdown("""
    ### 🔍 **Contract Obligation Extractor — Beyond Drafting AI**

    > This demo shows how AI can go beyond clause suggestions to help **extract actionable obligations from signed contracts** — something even top legal tools like Spellbook don't offer.

    **🎯 What Makes This Different:**
    - 🧠 **Real LLM Processing** — Uses actual OpenAI GPT-4 or Google Gemini APIs (no mock data)
    - 📄 **Post-Signature Analysis** — Extracts obligations from executed contracts, not just drafts
    - ⚠️ **Risk Assessment** — Automatically classifies obligations by risk level (Low/Medium/High)
    - 📊 **Actionable Output** — Structured data ready for compliance tracking and project management

    **🚀 Try It Now:**
    Upload any signed agreement and our AI will identify key obligations, deadlines, responsible parties, and potential risks — bridging the gap between **legal review** and **operational execution**.
    """)
    
    # Sidebar for system status
    render_sidebar()
    
    # Main content area
    render_main_content()

def render_sidebar():
    """Render sidebar with system status and information."""
    with st.sidebar:
        st.header("🔧 System Status")
        
        # Check API availability
        extractor = ObligationExtractor()
        system_status = extractor.get_system_status()
        
        # API Status
        st.subheader("API Status")
        apis = system_status["apis_available"]
        
        if apis["openai_available"]:
            st.success("✅ OpenAI GPT-4 Available")
        else:
            st.error("❌ OpenAI GPT-4 Not Available")
        
        if apis["gemini_available"]:
            st.success("✅ Google Gemini Available")
        else:
            st.error("❌ Google Gemini Not Available")
        
        if not apis["any_available"]:
            st.warning("⚠️ No LLM APIs available. Please check your API keys.")
        
        # System Status
        st.subheader("System Status")
        if system_status["system_ready"]:
            st.success("✅ System Ready")
        else:
            st.error("❌ System Not Ready")
        
        # Show which AI was used for last extraction
        if st.session_state.extraction_results and st.session_state.extraction_results["success"]:
            st.subheader("🤖 Last Processing")
            api_used = st.session_state.extraction_results["api_used"]
            obligations_count = st.session_state.extraction_results["total_obligations"]
            st.info(f"**{api_used}** extracted **{obligations_count} obligations**")
        
        # Information
        st.subheader("ℹ️ Information")
        st.info("""
        **How it works:**
        1. Upload a PDF or text contract
        2. AI analyzes the document
        3. Extract obligations with risk levels
        4. Download results as CSV
        
        **Supported formats:**
        - PDF files
        - Text files
        
        **Max file size:** 10MB
        """)

def render_main_content():
    """Render main content area."""
    
    # File upload section
    file_data = render_file_upload()
    
    # Demo contract section
    demo_text = render_demo_contract()
    
    # Process button
    if file_data or demo_text:
        st.divider()
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Extract Obligations", type="primary", use_container_width=True):
                process_contract(file_data, demo_text)

def process_contract(file_data: Optional[Tuple[bytes, str]], demo_text: Optional[str]):
    """Process the contract and extract obligations."""
    
    st.session_state.processing = True
    
    try:
        # Initialize extractor
        extractor = ObligationExtractor()
        
        # Check system status
        system_status = extractor.get_system_status()
        if not system_status["system_ready"]:
            st.error("❌ System not ready. Please check API keys.")
            return
        
        # Show processing status
        with st.status("Processing contract...", expanded=True) as status:
            st.write("📄 Extracting text from document...")
            
            # Process based on input type
            if file_data:
                file_content, file_type = file_data
                results = extractor.process_contract(file_content, file_type)
            elif demo_text:
                # For demo text, we need to encode it as bytes
                file_content = demo_text.encode('utf-8')
                results = extractor.process_contract(file_content, 'txt')
            else:
                st.error("No contract data provided.")
                return
            
            st.write(f"🤖 Analyzing with {results['api_used']}...")
            time.sleep(1)  # Simulate processing time
            
            st.write("📊 Extracting obligations...")
            time.sleep(1)
            
            if results["success"]:
                status.update(label=f"✅ Processing complete! ({results['api_used']} extracted {results['total_obligations']} obligations)", state="complete")
                st.session_state.extraction_results = results
            else:
                status.update(label="❌ Processing failed", state="error")
                st.error(f"Error: {results.get('error', 'Unknown error')}")
    
    except Exception as e:
        st.error(f"❌ Error processing contract: {str(e)}")
        logger.error(f"Processing error: {e}")
    
    finally:
        st.session_state.processing = False

def render_results():
    """Render extraction results."""
    if st.session_state.extraction_results and st.session_state.extraction_results["success"]:
        results = st.session_state.extraction_results
        
        # Display obligations table (this includes export options)
        render_obligations_table(results["obligations"])

def render_error_handling():
    """Render error handling and user guidance."""
    if st.session_state.processing:
        st.info("🔄 Processing contract... Please wait.")
        return
    
    # Show results if available
    if st.session_state.extraction_results:
        render_results()

if __name__ == "__main__":
    main()
    render_error_handling() 