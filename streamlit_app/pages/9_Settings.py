"""
===============================================================================
Project : Self-Healing Agentic AI ML Pipeline

File    : 9_Settings.py

Purpose :
Application Settings and Configuration

Author  : ChatGPT
===============================================================================
"""

from __future__ import annotations

import sys
from pathlib import Path
import os

import streamlit as st

# ==============================================================================
# Add Project Root
# ==============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ==============================================================================

import config

from utils.session import initialize_session_state

initialize_session_state()

# ==============================================================================
# Page Configuration
# ==============================================================================

st.set_page_config(

    page_title="Settings",

    page_icon="⚙️",

    layout="wide"

)

st.title("⚙️ Application Settings")

st.markdown("---")

# ==============================================================================
# Configuration
# ==============================================================================

st.subheader("Configuration")

config_data = {

    "Target Column": getattr(config, "TARGET_COLUMN", "N/A"),

    "Drift Threshold": getattr(config, "DRIFT_THRESHOLD", "N/A"),

    "Performance Threshold": getattr(config, "PERFORMANCE_THRESHOLD", "N/A"),

    "Log Level": getattr(config, "LOG_LEVEL", "N/A"),

    "SQLite Database": str(getattr(config, "SQLITE_DB_PATH", "N/A")),

    "Model Directory": str(getattr(config, "MODEL_DIR", "N/A"))

}

st.table(config_data)

# ==============================================================================
# Gemini
# ==============================================================================

st.markdown("---")

st.subheader("Gemini Configuration")

api_key = os.getenv("GEMINI_API_KEY")

model = os.getenv(

    "GEMINI_MODEL",

    "gemini-2.5-flash"

)

col1, col2 = st.columns(2)

with col1:

    st.metric(

        "Model",

        model

    )

with col2:

    if api_key:

        st.success("API Key Loaded")

    else:

        st.error("API Key Missing")

# ==============================================================================
# Session
# ==============================================================================

st.markdown("---")

st.subheader("Session State")

st.write(

    list(st.session_state.keys())

)

# ==============================================================================
# Clear Session
# ==============================================================================

if st.button(

    "Clear Session",

    use_container_width=True

):

    for key in list(st.session_state.keys()):

        del st.session_state[key]

    st.success(

        "Session cleared."

    )

# ==============================================================================
# About
# ==============================================================================

st.markdown("---")

st.subheader("About")

st.info(
"""
Self-Healing Agentic AI ML Pipeline

Features

• Dataset Validation

• Feature Engineering

• Model Prediction

• Drift Detection

• Performance Monitoring

• Gemini AI Diagnosis

• Autonomous Retraining

• Automatic Model Promotion

• Execution History

Version : 1.0
"""
)

# ==============================================================================
# Footer
# ==============================================================================

st.markdown("---")

st.caption(

    "© 2026 Self-Healing Agentic AI ML Pipeline"

)