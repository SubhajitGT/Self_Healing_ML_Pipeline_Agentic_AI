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

from utils.session_manager import initialize_session
from utils.workflow_manager import set_current_stage
from utils.page_guard import guard_validation
from utils.ui_components import page_header, page_footer
from utils.error_handler import show_error

initialize_session()
guard_validation()
set_current_stage("VALIDATION")

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

page_header(
    "✅ Dataset Validation",
    "Validate the uploaded dataset before monitoring."
)

# ==============================================================================
# Check Dataset
# ==============================================================================



dataframe = st.session_state.uploaded_df

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

        try:

            validator = DatasetValidator()

            validation_report = validator.validate(

        dataframe

    )
            if validation_report.get("status") == "FAILED":

                st.session_state.validated_df = None

        except Exception as exception:

            show_error(exception)

            st.stop()
        
        st.session_state.validation_report = (

            validation_report

        )
        st.session_state.validated_df = dataframe

    st.success(

        "Dataset validation completed successfully."

    )

# ==============================================================================
# Display Results
# ==============================================================================

if st.session_state.validation_report is not None:

    report = st.session_state.validation_report

    st.subheader("Validation Summary")

    status = report.get("status", "UNKNOWN")

    if status in ("PASS", "PASSED"):

        st.success("Dataset passed validation.")

    elif status.upper() == "WARNING":

        st.warning("Dataset passed with warnings.")

    elif status in ("FAIL", "FAILED"):

        st.error("Dataset failed validation.")

    else:

        st.info(f"Validation status: {status}")

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

        report,
        expanded=True

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
    page_footer()