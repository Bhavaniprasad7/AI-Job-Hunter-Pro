#!/usr/bin/env python
"""
Streamlit entry point for AI Job Hunter Pro.
Streamlit Cloud automatically looks for streamlit_app.py in the root.
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from ai_job_hunter_pro.ui.streamlit_app import render_dashboard

if __name__ == "__main__":
    render_dashboard()
