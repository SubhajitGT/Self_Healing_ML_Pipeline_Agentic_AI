"""
===============================================================================
Project : Self-Healing Agentic AI ML Pipeline

File    : app.py

Purpose :
Main Streamlit Application.

Author  : ChatGPT
===============================================================================
"""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st
from components.sidebar import render_sidebar

from utils.session import initialize_session_state

initialize_session_state()

# ==============================================================================
# Add Project Root
# ==============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ==============================================================================

import config

# ==============================================================================
# Streamlit Configuration
# ==============================================================================

st.set_page_config(

    page_title="Self-Healing ML Pipeline",

    page_icon="🤖",

    layout="wide",

    initial_sidebar_state="expanded"

)
render_sidebar()

# ==============================================================================
# Session State
# ==============================================================================

if "uploaded_dataframe" not in st.session_state:

    st.session_state.uploaded_dataframe = None

if "validation_report" not in st.session_state:

    st.session_state.validation_report = None

if "prediction_result" not in st.session_state:

    st.session_state.prediction_result = None

if "drift_report" not in st.session_state:

    st.session_state.drift_report = None

if "performance_report" not in st.session_state:

    st.session_state.performance_report = None

if "ai_report" not in st.session_state:

    st.session_state.ai_report = None

if "self_healing_report" not in st.session_state:

    st.session_state.self_healing_report = None

# ==============================================================================
# Header
# ==============================================================================

st.title("🤖 Self-Healing Agentic AI ML Pipeline")

st.markdown("---")

st.markdown(
    """
Welcome to the **Self-Healing Agentic AI ML Pipeline**.

This application demonstrates an end-to-end intelligent ML system capable of:

- 📂 Uploading datasets
- ✅ Validating data quality
- 📊 Running predictions
- 📈 Detecting drift
- 📉 Monitoring model performance
- 🧠 AI-powered diagnosis using Gemini
- ⚙️ Automatic self-healing and model retraining
"""
)


st.success(
    "Welcome! Use the navigation menu on the left to explore the application."
)

st.info(
    """
The dashboard pages are available from the sidebar.

Start with **🏠 Dashboard**.
"""
)