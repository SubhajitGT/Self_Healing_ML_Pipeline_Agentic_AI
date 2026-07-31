"""
===============================================================================
Project : Self-Healing Agentic AI ML Pipeline

File    : 1_Home.py

Purpose :
Home Dashboard

Author  : ChatGPT
===============================================================================
"""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

from utils.session_manager import initialize_session

initialize_session()

# ==============================================================================
# Add Project Root
# ==============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ==============================================================================

import config

# ==============================================================================
# Page
# ==============================================================================

st.set_page_config(

    page_title="Dashboard",

    page_icon="🏠",

    layout="wide"

)

st.title("🏠 Dashboard")

st.markdown("---")

# ==============================================================================
# KPI Cards
# ==============================================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(

        "Current Model",

        "Version 1"

    )

with col2:

    st.metric(

        "Pipeline Status",

        "Healthy"

    )

with col3:

    st.metric(

        "AI Diagnosis",

        "Ready"

    )

with col4:

    st.metric(

        "Self-Healing",

        "Enabled"

    )

st.markdown("---")

# ==============================================================================
# Project Overview
# ==============================================================================

st.subheader("📌 Project Overview")

st.info(
    """
This project demonstrates an **Agentic AI based Self-Healing Machine Learning
Pipeline**.

The system automatically:

• Validates datasets

• Generates predictions

• Detects data drift

• Monitors performance

• Diagnoses issues using Gemini AI

• Retrains the model automatically

• Promotes the better model

• Maintains execution history
"""
)

# ==============================================================================
# Workflow
# ==============================================================================

st.subheader("🔄 Pipeline Workflow")

st.code(
"""
Dataset
   │
   ▼
Validation
   │
   ▼
Feature Engineering
   │
   ▼
Prediction
   │
   ▼
Performance Monitoring
   │
   ▼
Drift Detection
   │
   ▼
Gemini AI Diagnosis
   │
   ▼
Self-Healing
   │
   ▼
Model Promotion
""",
language="text"
)

# ==============================================================================
# Module Status
# ==============================================================================

st.subheader("📊 Module Status")

status = {

    "Data Generation":"✅ Completed",

    "Database":"✅ Completed",

    "Machine Learning":"✅ Completed",

    "Monitoring":"✅ Completed",

    "Agentic AI":"✅ Completed",

    "Self-Healing":"✅ Completed",

    "Streamlit":"✅ Completed"

}

st.table(status)

# ==============================================================================
# Footer
# ==============================================================================

st.markdown("---")

st.caption(
    "Self-Healing Agentic AI ML Pipeline | Version 1.0"
)