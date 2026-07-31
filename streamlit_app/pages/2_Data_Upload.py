"""
===============================================================================
Project : Self-Healing Agentic AI ML Pipeline

File    : 2_Data_Upload.py

Purpose :
Upload and Preview Dataset

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
from utils.ui_components import page_header, page_footer
from utils.error_handler import show_error

initialize_session()
set_current_stage("UPLOAD")

# ==============================================================================
# Add Project Root
# ==============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ==============================================================================

st.set_page_config(

    page_title="Dataset Upload",

    page_icon="📂",

    layout="wide"

)

page_header(
    "📂 Upload Dataset",
    "Upload a CSV or Excel dataset."
)

# ==============================================================================
# File Upload
# ==============================================================================

uploaded_file = st.file_uploader(

    "Upload CSV or Excel",

    type=["csv", "xlsx"]

)

# ==============================================================================
# Load Dataset
# ==============================================================================

if uploaded_file is not None:

    try:

        if uploaded_file.name.endswith(".csv"):

            dataframe = pd.read_csv(

                uploaded_file

            )

        else:

            dataframe = pd.read_excel(

                uploaded_file

            )

        st.session_state.uploaded_df = dataframe
        st.session_state.uploaded_filename = uploaded_file.name
        # Reset downstream state

        from utils.session_manager import reset_workflow

        reset_workflow()

        st.session_state.uploaded_df = dataframe
        st.session_state.uploaded_filename = uploaded_file.name
        st.success(

            "Dataset uploaded successfully."

        )
        st.info(
    f"""
Filename : {uploaded_file.name}

Rows : {len(dataframe)}

Columns : {len(dataframe.columns)}
"""
)

    except Exception as exception:

        show_error(
        exception,
        show_traceback=True
    )

# ==============================================================================
# Preview
# ==============================================================================

if st.session_state.uploaded_df is not None:

    dataframe = st.session_state.uploaded_df

    st.subheader("Dataset Preview")

    st.dataframe(

        dataframe,

        use_container_width=True

    )

    st.markdown("---")

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

        memory = round(

            dataframe.memory_usage(

                deep=True

            ).sum() / 1024,

            2

        )

        st.metric(

            "Memory (KB)",

            memory

        )

    st.markdown("---")

    st.subheader("Column Information")

    info_df = pd.DataFrame({

        "Column": dataframe.columns,

        "Data Type": dataframe.dtypes.astype(str),

        "Missing Values": dataframe.isnull().sum().values

    })

    st.dataframe(

        info_df,

        use_container_width=True

    )
    page_footer()