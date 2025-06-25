#!/usr/bin/env python3
"""
Streamlit entry point for Contract Obligation Extractor.
This file serves as the main entry point for Streamlit Cloud deployment.
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path for proper imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import and run the main application
exec(open('app/main.py').read()) 