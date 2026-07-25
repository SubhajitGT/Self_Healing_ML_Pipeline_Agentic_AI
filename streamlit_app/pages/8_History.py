"""
===============================================================================
Project : Self-Healing Agentic AI ML Pipeline

File    : 8_History.py

Purpose :
Execution History Dashboard

Author  : ChatGPT
===============================================================================
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

# ==============================================================================
# Add Project Root
# ==============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ==============================================================================

from self_healing.history_manager import HistoryManager
from utils.session import initialize_session_state

initialize_session_state()

# ==============================================================================
# Page Configuration
# ==============================================================================

st.set_page_config(

    page_title="Execution History",

    page_icon="📜",

    layout="wide"

)

st.title("📜 Self-Healing Execution History")

st.markdown("---")

# ==============================================================================
# Load History
# ==============================================================================

history_manager = HistoryManager()

history = history_manager.get_history()

if len(history) == 0:

    st.info(

        "No execution history available."

    )

    st.stop()

history_df = pd.DataFrame(history)

# ==============================================================================
# Sidebar Filters
# ==============================================================================

st.sidebar.header("Filters")

severity_options = ["All"] + sorted(

    history_df["severity"].dropna().unique().tolist()

)

selected_severity = st.sidebar.selectbox(

    "Severity",

    severity_options

)

action_options = ["All"] + sorted(

    history_df["action"].dropna().unique().tolist()

)

selected_action = st.sidebar.selectbox(

    "Action",

    action_options

)

# ==============================================================================
# Apply Filters
# ==============================================================================

filtered_df = history_df.copy()

if selected_severity != "All":

    filtered_df = filtered_df[

        filtered_df["severity"] == selected_severity

    ]

if selected_action != "All":

    filtered_df = filtered_df[

        filtered_df["action"] == selected_action

    ]

# ==============================================================================
# Summary
# ==============================================================================

st.subheader("Execution Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(

        "Total Executions",

        len(filtered_df)

    )

with col2:

    promoted = int(

        filtered_df["promoted"].sum()

    )

    st.metric(

        "Promotions",

        promoted

    )

with col3:

    latest_version = filtered_df["new_version"].max()

    st.metric(

        "Latest Version",

        latest_version

    )

with col4:

    latest_timestamp = filtered_df.iloc[0]["timestamp"]

    st.metric(

        "Latest Execution",

        latest_timestamp

    )

st.markdown("---")

# ==============================================================================
# History Table
# ==============================================================================

st.subheader("Execution Records")

display_columns = [

    "timestamp",

    "severity",

    "action",

    "promoted",

    "old_version",

    "new_version",

    "reason"

]

st.dataframe(

    filtered_df[display_columns],

    use_container_width=True,

    hide_index=True

)

# ==============================================================================
# Metrics Comparison
# ==============================================================================

st.markdown("---")

st.subheader("Execution Details")

selected_index = st.selectbox(

    "Select Execution",

    filtered_df.index,

    format_func=lambda idx:
        filtered_df.loc[idx, "timestamp"]

)

record = filtered_df.loc[selected_index]

col1, col2 = st.columns(2)

with col1:

    st.write("### Candidate Metrics")

    st.json(

        record["candidate_metrics"]

    )

with col2:

    st.write("### Production Metrics")

    st.json(

        record["production_metrics"]

    )

# ==============================================================================
# Download
# ==============================================================================

csv = filtered_df.to_csv(

    index=False

).encode("utf-8")

st.download_button(

    "Download History",

    data=csv,

    file_name="execution_history.csv",

    mime="text/csv"

)