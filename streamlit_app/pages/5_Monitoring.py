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

from monitoring.drift_detector import DriftDetector
from monitoring.performance_monitor import PerformanceMonitor

from data.generator import SalesDataGenerator

from utils.session_manager import initialize_session
from utils.workflow_manager import set_current_stage
from utils.page_guard import guard_monitoring
from utils.ui_components import page_header, page_footer
from utils.error_handler import show_error

initialize_session()

guard_monitoring()

set_current_stage("MONITORING")

# ==============================================================================
# Page Configuration
# ==============================================================================

st.set_page_config(

    page_title="Monitoring",

    page_icon="📊",

    layout="wide"

)

page_header(
    "📊 Monitoring Dashboard",
    "Monitor dataset quality, drift and production model health."
)

# ==============================================================================
# Dataset Check
# ==============================================================================
current_df = st.session_state.validated_df

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


        drift_detector = DriftDetector()

        performance_monitor = PerformanceMonitor()

        # ---------------------------------------------------------
        # Validation
        # ---------------------------------------------------------

        validation_report = st.session_state.validation_report

        # ---------------------------------------------------------
        # Generate Reference Dataset
        # ---------------------------------------------------------

        generator = SalesDataGenerator(

            rows=len(current_df)

        )

        reference_df = generator.generate_dataset()

        # ---------------------------------------------------------
        # Drift Detection
        # ---------------------------------------------------------

        drift_report = drift_detector.detect(

            reference_df,

            current_df

        )

        # ---------------------------------------------------------
        # Demo Performance Metrics
        #
        # Later these will come from the production model
        # and current prediction evaluation.
        # ---------------------------------------------------------

        previous_metrics = {

            "mae": 10.20,

            "rmse": 15.40,

            "r2": 0.962

        }

        current_metrics = {

            "mae": 12.75,

            "rmse": 18.60,

            "r2": 0.935

        }

        performance_report = performance_monitor.monitor(

            previous_metrics,

            current_metrics

        )

        # ---------------------------------------------------------
        # Save Reports
        # ---------------------------------------------------------

        st.session_state.validation_report = validation_report

        st.session_state.drift_report = drift_report

        st.session_state.performance_report = performance_report
        st.session_state.monitoring_report = {

    "validation": validation_report,

    "drift": drift_report,

    "performance": performance_report

}

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

    st.markdown("---")

    st.subheader("✅ Dataset Validation")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(

            "Rows",

            len(current_df)

        )

    with col2:

        st.metric(

            "Columns",

            len(current_df.columns)

        )

    with col3:

        st.metric(

            "Status",

            validation_report.get(

                "status",

                "UNKNOWN"

            )

        )

    st.json(

        validation_report,
        expanded=True

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

    if drift_report.get(

        "drift_detected",

        False

    ):

        st.error(

            "Drift detected."

        )

    else:

        st.success(

            "No significant drift detected."

        )

    st.json(

        drift_report,
        expanded=True

    )

# ==============================================================================
# Performance Monitoring
# ==============================================================================

performance_report = st.session_state.get(

    "performance_report"

)

if performance_report is not None:

    st.markdown("---")

    st.subheader("📈 Performance Monitoring")

    summary = performance_report.get(

        "summary",

        {}

    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(

            "MAE",

            summary.get(

                "current_mae",

                "-"

            )

        )

    with col2:

        st.metric(

            "RMSE",

            summary.get(

                "current_rmse",

                "-"

            )

        )

    with col3:

        st.metric(

            "R²",

            summary.get(

                "current_r2",

                "-"

            )

        )

    st.json(

        performance_report,
        expanded=True

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

    health_score = performance_report["health_score"]

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

    report = st.session_state.monitoring_report

    st.markdown("---")

    st.download_button(

        label="📥 Download Monitoring Report",

        data=str(report),

        file_name="monitoring_report.txt",

        mime="text/plain",

        use_container_width=True

    )
    page_footer()