"""
===============================================================================
Project : Self-Healing Agentic AI ML Pipeline

File    : 7_Self_Healing.py

Purpose :
Run complete self-healing workflow.

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


from utils.session import initialize_session_state

initialize_session_state()

from self_healing.orchestrator import SelfHealingOrchestrator
# ==============================================================================
# Page
# ==============================================================================

st.set_page_config(

    page_title="Self-Healing",

    page_icon="⚙️",

    layout="wide"

)

st.title("⚙️ Self-Healing")

st.markdown("---")

# ==============================================================================
# Check Required Data
# ==============================================================================

dataframe = st.session_state.get("uploaded_dataframe")

ai_report = st.session_state.get("ai_report")

if dataframe is None:

    st.warning("Please upload a dataset.")

    st.stop()

if ai_report is None:

    st.warning("Please run AI Diagnosis first.")

    st.stop()

# ==============================================================================
# Production Metrics
# ==============================================================================

performance_report = st.session_state.get(
    "performance_report"
)

if performance_report is None:

    st.warning("Performance report not available.")

    st.stop()

production_metrics = {

    "mae": performance_report.get("mae", 0),

    "rmse": performance_report.get("rmse", 0),

    "r2": performance_report.get("r2", 0)

}

# ==============================================================================
# Execute
# ==============================================================================

if st.button(

    "Run Self-Healing",

    use_container_width=True,

    type="primary"

):

    progress = st.progress(0)

    status = st.empty()

    # ----------------------------------------------------------

    status.info("Decision Engine...")

    progress.progress(15)

    orchestrator = SelfHealingOrchestrator()

    # ----------------------------------------------------------

    status.info("Executing workflow...")

    progress.progress(50)

    result = orchestrator.execute(

        dataframe=dataframe,

        ai_report=ai_report,

        production_metrics=production_metrics,

        current_version=1

    )

    # ----------------------------------------------------------

    progress.progress(100)

    status.success("Self-Healing completed.")

    st.session_state.self_healing_report = result

# ==============================================================================
# Display Result
# ==============================================================================

result = st.session_state.get(

    "self_healing_report"

)

if result is not None:

    st.markdown("---")

    st.subheader("Workflow Summary")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(

            "Workflow",

            result["workflow_status"]

        )

    with col2:

        st.metric(

            "Retrained",

            "YES"

            if result["retrained"]

            else

            "NO"

        )

    with col3:

        if result["promotion"]:

            promoted = result["promotion"]["promoted"]

            st.metric(

                "Promoted",

                "YES"

                if promoted

                else

                "NO"

            )

        else:

            st.metric(

                "Promoted",

                "N/A"

            )

# ==============================================================================
# Decision
# ==============================================================================

    st.markdown("---")

    st.subheader("Decision")

    st.json(

        result["decision"]

    )

# ==============================================================================
# Candidate Metrics
# ==============================================================================

    if result["retrained"]:

        metrics = result["candidate"][

            "candidate_metrics"

        ]

        st.markdown("---")

        st.subheader(

            "Candidate Model Metrics"

        )

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(

                "MAE",

                round(

                    metrics["mae"],

                    4

                )

            )

        with c2:

            st.metric(

                "RMSE",

                round(

                    metrics["rmse"],

                    4

                )

            )

        with c3:

            st.metric(

                "R²",

                round(

                    metrics["r2"],

                    4

                )

            )

# ==============================================================================
# Promotion Report
# ==============================================================================

    if result["promotion"]:

        promotion = result["promotion"]

        st.markdown("---")

        st.subheader(

            "Promotion Decision"

        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(

                "Old Version",

                promotion["old_version"]

            )

        with col2:

            st.metric(

                "New Version",

                promotion["new_version"]

            )

        st.success(

            promotion["reason"]

        )

# ==============================================================================
# Raw Report
# ==============================================================================

    st.markdown("---")

    with st.expander(

        "Execution Report"

    ):

        st.json(result)

# ==============================================================================
# Download
# ==============================================================================

    st.download_button(

        "Download Execution Report",

        data=str(result),

        file_name="self_healing_report.txt",

        mime="text/plain"

    )