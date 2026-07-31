"""
===============================================================================
Project : Self-Healing Agentic AI ML Pipeline

File    : session_manager.py

Purpose :
Centralized Streamlit session state management.

Author  : ChatGPT
===============================================================================
"""

from __future__ import annotations

import streamlit as st


# ==============================================================================
# Default Session Variables
# ==============================================================================

DEFAULT_SESSION = {

    # ------------------------------------------------------------------
    # Dataset
    # ------------------------------------------------------------------

    "uploaded_df": None,

    "validated_df": None,

    "prediction_df": None,

    # ------------------------------------------------------------------
    # Reports
    # ------------------------------------------------------------------

    "validation_report": None,

    "monitoring_report": None,

    "ai_report": None,

    "self_healing_result": None,

    "prediction_result": None,

    # ------------------------------------------------------------------
    # Model
    # ------------------------------------------------------------------

    "current_model_version": 1,

    "candidate_model_version": None,

    # ------------------------------------------------------------------
    # Workflow
    # ------------------------------------------------------------------

    "workflow_stage": "HOME",

    "workflow_completed": False,

    # ------------------------------------------------------------------
    # UI
    # ------------------------------------------------------------------

    "processing": False,

    "last_error": None

}


# ==============================================================================
# Initialize Session
# ==============================================================================

def initialize_session() -> None:
    """
    Initialize Streamlit session state.
    """

    for key, value in DEFAULT_SESSION.items():

        if key not in st.session_state:

            st.session_state[key] = value


# ==============================================================================
# Reset Workflow
# ==============================================================================

def reset_workflow() -> None:
    """
    Reset workflow related session variables.
    """

    workflow_keys = [

        "uploaded_df",

        "validated_df",

        "prediction_df",

        "validation_report",

        "monitoring_report",

        "ai_report",

        "self_healing_result",

        "prediction_result",

        "candidate_model_version",

        "workflow_stage",

        "workflow_completed",

        "processing",

        "last_error"

    ]

    for key in workflow_keys:

        st.session_state[key] = DEFAULT_SESSION[key]


# ==============================================================================
# Reset Entire Session
# ==============================================================================

def reset_session() -> None:
    """
    Reset complete session.
    """

    for key, value in DEFAULT_SESSION.items():

        st.session_state[key] = value