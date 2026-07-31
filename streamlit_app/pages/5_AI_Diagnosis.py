"""
===============================================================================
Project : Self-Healing Agentic AI ML Pipeline

File    : 6_AI_Diagnosis.py

Purpose :
AI Diagnosis Dashboard

Author  : ChatGPT
===============================================================================
"""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

# ==============================================================================
# Add Project Root
# ==============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ==============================================================================

from agents.orchestrator import AIOrchestrator
from utils.session import initialize_session_state

initialize_session_state()

# ==============================================================================
# Page
# ==============================================================================

st.set_page_config(

    page_title="AI Diagnosis",

    page_icon="🧠",

    layout="wide"

)

st.title("🧠 AI Diagnosis")

st.markdown("---")

# ==============================================================================
# Check Monitoring Reports
# ==============================================================================

validation_report = st.session_state.get("validation_report")

drift_report = st.session_state.get("drift_report")

performance_report = st.session_state.get("performance_report")

if (

    validation_report is None

    or drift_report is None

    or performance_report is None

):

    st.warning(

        "Please run the Monitoring Dashboard first."

    )

    st.stop()

# ==============================================================================
# AI Diagnosis
# ==============================================================================

if st.button(

    "Run AI Diagnosis",

    use_container_width=True

):

    with st.spinner(

        "AI is analysing the pipeline..."

    ):

        orchestrator = AIOrchestrator()

        ai_report = orchestrator.analyze(

            validation_report=validation_report,

            drift_report=drift_report,

            performance_report=performance_report

        )

        st.session_state.ai_report = ai_report

    st.success(

        "AI diagnosis completed."

    )

# ==============================================================================
# Display Report
# ==============================================================================

ai_report = st.session_state.get(

    "ai_report"

)

if ai_report is not None:

    summary = ai_report.get(

        "summary",

        {}

    )

    st.subheader("Executive Summary")

    st.info(

        summary.get(

            "summary",

            "No summary available."

        )

    )

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(

            "Severity",

            summary.get(

                "severity",

                "UNKNOWN"

            )

        )

    with col2:

        st.metric(

            "Confidence",

            summary.get(

                "confidence",

                "N/A"

            )

        )

    with col3:

        recommendation = ai_report.get(

            "retraining",

            {}

        ).get(

            "required",

            False

        )

        st.metric(

            "Retraining",

            "YES" if recommendation else "NO"

        )

    st.markdown("---")

    st.subheader("Root Cause")

    st.write(

        ai_report.get(

            "root_cause",

            "No root cause identified."

        )

    )

    st.markdown("---")

    st.subheader("Business Impact")

    st.write(

        ai_report.get(

            "business_impact",

            "No business impact available."

        )

    )

    st.markdown("---")

    st.subheader("Recommendations")

    recommendations = ai_report.get(

        "recommendations",

        []

    )

    if isinstance(recommendations, list):

        for item in recommendations:

            st.write(f"• {item}")

    else:

        st.write(recommendations)

    st.markdown("---")

    st.subheader("Raw AI Report")

    st.json(

        ai_report

    )

    st.download_button(

        "Download AI Report",

        data=str(ai_report),

        file_name="ai_diagnosis.txt",

        mime="text/plain"

    )
