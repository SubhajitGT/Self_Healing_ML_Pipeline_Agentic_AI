"""
===============================================================================
Project : Self-Healing Agentic AI ML Pipeline

File    : 5_Monitoring.py

Purpose :
Model Monitoring Dashboard

Author  : ChatGPT
===============================================================================
"""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st
import pandas as pd

# ==============================================================================
# Add Project Root
# ==============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ==============================================================================

from monitoring.validator import DatasetValidator
from monitoring.drift_detector import DriftDetector
from monitoring.performance_monitor import PerformanceMonitor

from utils.session import initialize_session_state

initialize_session_state()

# ==============================================================================
# Page Configuration
# ==============================================================================

st.set_page_config(

    page_title="Monitoring",

    page_icon="📊",

    layout="wide"

)

st.title("📊 Monitoring Dashboard")

st.markdown("---")

# ==============================================================================
# Dataset Check
# ==============================================================================

dataframe = st.session_state.get(

    "uploaded_dataframe"

)

if dataframe is None:

    st.warning(

        "Please upload a dataset first."

    )

    st.stop()

# ==============================================================================
# Run Monitoring
# ==============================================================================

if st.button(

    "Run Monitoring",

    use_container_width=True

):

    with st.spinner(

        "Running monitoring pipeline..."

    ):

        validator = DatasetValidator()

        drift_detector = DriftDetector()

        performance_monitor = PerformanceMonitor()

        # ---------------------------------------------------------
        # Validation
        # ---------------------------------------------------------

        validation_report = validator.validate(

            dataframe

        )

        # ---------------------------------------------------------
        # Drift Detection
        # ---------------------------------------------------------

        drift_report = drift_detector.detect_category_drift(

            dataframe

        )

        # ---------------------------------------------------------
        # Performance Monitoring
        # ---------------------------------------------------------

        performance_report = performance_monitor.monitor(

            dataframe

        )

        st.session_state.validation_report = validation_report

        st.session_state.drift_report = drift_report

        st.session_state.performance_report = performance_report

    st.success(

        "Monitoring completed successfully."

    )

# ==============================================================================
# Validation Summary
# ==============================================================================

validation_report = st.session_state.get(

    "validation_report"

)

if validation_report is not None:

    st.subheader("✅ Dataset Validation")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(

            "Rows",

            len(dataframe)

        )

    with col2:

        st.metric(

            "Columns",

            len(dataframe.columns)

        )

    with col3:

        st.metric(

            "Status",

            validation_report.get(

                "status",

                "UNKNOWN"

            )

        )

# ==============================================================================
# Drift Detection
# ==============================================================================

drift_report = st.session_state.get(

    "drift_report"

)

if drift_report is not None:

    st.markdown("---")

    st.subheader("📉 Drift Detection")

    st.json(

        drift_report

    )

# ==============================================================================
# Performance Monitoring
# ==============================================================================

performance_report = st.session_state.get(

    "performance_report"

)

if performance_report is not None:

    st.markdown("---")

    st.subheader("📈 Performance Metrics")

    st.json(

        performance_report

    )

# ==============================================================================
# Overall Health
# ==============================================================================

if (

    validation_report is not None

    and drift_report is not None

    and performance_report is not None

):

    st.markdown("---")

    st.subheader("🟢 Overall Pipeline Health")

    health_score = 100

    if validation_report.get("status") != "PASS":

        health_score -= 30

    if drift_report.get("drift_detected", False):

        health_score -= 40

    if performance_report.get("status", "").upper() != "HEALTHY":

        health_score -= 30

    health_score = max(0, health_score)

    st.progress(

        health_score / 100

    )

    st.metric(

        "Health Score",

        f"{health_score}%"

    )

# ==============================================================================
# Download Report
# ==============================================================================

if (

    validation_report is not None

    and drift_report is not None

    and performance_report is not None

):

    report = {

        "validation": validation_report,

        "drift": drift_report,

        "performance": performance_report

    }

    st.download_button(

        "Download Monitoring Report",

        data=str(report),

        file_name="monitoring_report.txt",

        mime="text/plain"

    )