"""
===============================================================================
Project : Self-Healing Agentic AI ML Pipeline

File    : 3_Data_Validation.py

Purpose :
Validate uploaded dataset.

Author  : ChatGPT
===============================================================================
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

from utils.session import initialize_session_state

initialize_session_state()

# ==============================================================================
# Add Project Root
# ==============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ==============================================================================

from monitoring.validator import DatasetValidator

# ==============================================================================
# Page Configuration
# ==============================================================================

st.set_page_config(

    page_title="Data Validation",

    page_icon="✅",

    layout="wide"

)

st.title("✅ Dataset Validation")

st.markdown("---")

# ==============================================================================
# Check Dataset
# ==============================================================================

if st.session_state.uploaded_dataframe is None:

    st.warning(

        "Please upload a dataset first."

    )

    st.stop()

dataframe = st.session_state.uploaded_dataframe

# ==============================================================================
# Run Validation
# ==============================================================================

if st.button(

    "Run Validation",

    use_container_width=True

):

    with st.spinner(

        "Validating dataset..."

    ):

        validator = DatasetValidator()

        validation_report = validator.validate(

            dataframe

        )

        st.session_state.validation_report = (

            validation_report

        )

    st.success(

        "Validation completed successfully."

    )

# ==============================================================================
# Display Results
# ==============================================================================

if st.session_state.validation_report is not None:

    report = st.session_state.validation_report

    st.subheader("Validation Summary")

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

        status = report.get(

            "status",

            "UNKNOWN"

        )

        st.metric(

            "Status",

            status

        )

    st.markdown("---")

    st.subheader("Validation Report")

    st.json(

        report

    )

    st.markdown("---")

    st.subheader("Dataset Preview")

    st.dataframe(

        dataframe.head(20),

        use_container_width=True

    )

    st.download_button(

        label="Download Validation Report",

        data=str(report),

        file_name="validation_report.txt",

        mime="text/plain"

    )