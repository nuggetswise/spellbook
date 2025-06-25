#!/usr/bin/env python3
"""
Launcher script for Contract Obligation Extractor.
This script ensures proper module imports and launches the Streamlit app.
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import and run the main application
if __name__ == "__main__":
    import streamlit.web.cli as stcli
    
    # Set the script path to the main.py file
    script_path = str(current_dir / "app" / "main.py")
    
    # Run streamlit
    sys.argv = ["streamlit", "run", script_path, "--server.port=8501", "--server.address=localhost"]
    sys.exit(stcli.main()) 