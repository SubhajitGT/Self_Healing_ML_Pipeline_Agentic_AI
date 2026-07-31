"""
===============================================================================
Project : Self-Healing Agentic AI ML Pipeline

File    : page_guard.py

Purpose :
Protect Streamlit pages from invalid workflow navigation.

Author  : ChatGPT
===============================================================================
"""

from __future__ import annotations

import streamlit as st

from .workflow_manager import can_access


# ==============================================================================
# Guard Page
# ==============================================================================

def guard_page(
    stage: str,
    message: str
) -> None:
    """
    Prevent access to a page when workflow prerequisites
    are not satisfied.
    """

    if can_access(stage):

        return

    st.warning(message)

    st.stop()


# ==============================================================================
# Page Guards
# ==============================================================================

def guard_validation() -> None:

    guard_page(

        "VALIDATION",

        "⚠ Please upload a dataset before opening this page."

    )


def guard_explorer() -> None:

    guard_page(

        "EXPLORER",

        "⚠ Please validate the uploaded dataset first."

    )


def guard_monitoring() -> None:

    guard_page(

        "MONITORING",

        "⚠ Please validate the uploaded dataset before monitoring."

    )


def guard_ai() -> None:

    guard_page(

        "AI_DIAGNOSIS",

        "⚠ Please complete Monitoring before AI Diagnosis."

    )


def guard_self_healing() -> None:

    guard_page(

        "SELF_HEALING",

        "⚠ Please complete AI Diagnosis before Self-Healing."

    )


def guard_model_evolution() -> None:

    guard_page(

        "MODEL_EVOLUTION",

        "⚠ Please complete Self-Healing before viewing Model Evolution."

    )


def guard_prediction() -> None:

    guard_page(

        "PREDICTION",

        "⚠ Please upload and validate a dataset before Prediction."

    )


def guard_history() -> None:

    guard_page(

        "HISTORY",

        "⚠ No execution history available."

    )