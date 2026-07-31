"""
===============================================================================
Project : Self-Healing Agentic AI ML Pipeline

File    : workflow_manager.py

Purpose :
Manage dashboard workflow stages and page access.

Author  : ChatGPT
===============================================================================
"""

from __future__ import annotations

import streamlit as st

import config


# ==============================================================================
# Workflow Stages
# ==============================================================================

WORKFLOW_STAGES = config.WORKFLOW_STAGES

# ==============================================================================
# Current Workflow Stage
# ==============================================================================

def get_current_stage() -> str:
    """
    Return current workflow stage.
    """

    return st.session_state.get(

        "workflow_stage",

        "HOME"

    )


# ==============================================================================
# Update Workflow Stage
# ==============================================================================

def set_current_stage(
    stage: str
) -> None:
    """
    Update workflow stage.
    """

    if stage not in WORKFLOW_STAGES:

        raise ValueError(

            f"Invalid workflow stage: {stage}"

        )

    st.session_state["workflow_stage"] = stage


# ==============================================================================
# Stage Completed
# ==============================================================================

def mark_workflow_completed() -> None:
    """
    Mark workflow as completed.
    """

    st.session_state["workflow_completed"] = True


# ==============================================================================
# Reset Workflow
# ==============================================================================

def reset_workflow_stage() -> None:
    """
    Reset workflow stage.
    """

    st.session_state["workflow_stage"] = "HOME"

    st.session_state["workflow_completed"] = False


# ==============================================================================
# Page Access Rules
# ==============================================================================

def can_access_upload() -> bool:

    return True


def can_access_validation() -> bool:

    return st.session_state.get(

        "uploaded_df"

    ) is not None


def can_access_explorer() -> bool:

    return st.session_state.get(

        "validated_df"

    ) is not None


def can_access_monitoring() -> bool:

    return st.session_state.get(

        "validated_df"

    ) is not None


def can_access_ai() -> bool:

    return st.session_state.get(

        "monitoring_report"

    ) is not None


def can_access_self_healing() -> bool:

    return st.session_state.get(

        "ai_report"

    ) is not None


def can_access_model_evolution() -> bool:

    return st.session_state.get(

        "self_healing_result"

    ) is not None


def can_access_prediction() -> bool:

    return st.session_state.get(

        "validated_df"

    ) is not None


def can_access_history() -> bool:

    return True

# ==============================================================================
# Generic Access Check
# ==============================================================================

ACCESS_RULES = {

    "UPLOAD": can_access_upload,

    "VALIDATION": can_access_validation,

    "EXPLORER": can_access_explorer,

    "MONITORING": can_access_monitoring,

    "AI_DIAGNOSIS": can_access_ai,

    "SELF_HEALING": can_access_self_healing,

    "MODEL_EVOLUTION": can_access_model_evolution,

    "PREDICTION": can_access_prediction,

    "HISTORY": can_access_history

}


def can_access(
    stage: str
) -> bool:
    """
    Generic page access validator.
    """

    if stage not in ACCESS_RULES:

        raise ValueError(

            f"Unknown workflow stage: {stage}"

        )

    return ACCESS_RULES[stage]()