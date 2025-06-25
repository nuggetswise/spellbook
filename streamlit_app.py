#!/usr/bin/env python3
"""
Streamlit entry point for Contract Obligation Extractor.
This file is the main entry point for Streamlit Cloud deployment.
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path for proper imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import the main app module and run it
from app.main import main, render_error_handling

# Run the main application
if __name__ == "__main__":
    main()
    render_error_handling() 