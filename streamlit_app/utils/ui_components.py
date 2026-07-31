"""
===============================================================================
Project : Self-Healing Agentic AI ML Pipeline

File    : ui_components.py

Purpose :
Reusable Streamlit UI components used across all dashboard pages.

Author  : ChatGPT
===============================================================================
"""

from __future__ import annotations

import streamlit as st
import config

# ==============================================================================
# Workflow Progress Mapping
# ==============================================================================

STAGE_PROGRESS = config.WORKFLOW_PROGRESS
# ==============================================================================
# Page Header
# ==============================================================================

def page_header(
    title: str,
    description: str | None = None
) -> None:
    """
    Display a standard page header.
    """

    st.title(title)

    if description:

        st.caption(description)

    st.markdown("---")


# ==============================================================================
# Section Header
# ==============================================================================

def section_header(
    title: str
) -> None:
    """
    Display a standard section title.
    """

    st.subheader(title)


# ==============================================================================
# Success Message
# ==============================================================================

def success_message(
    message: str
) -> None:
    """
    Display success message.
    """

    st.success(message)


# ==============================================================================
# Warning Message
# ==============================================================================

def warning_message(
    message: str
) -> None:
    """
    Display warning message.
    """

    st.warning(message)


# ==============================================================================
# Error Message
# ==============================================================================

def error_message(
    message: str
) -> None:
    """
    Display error message.
    """

    st.error(message)


# ==============================================================================
# Information Message
# ==============================================================================

def info_message(
    message: str
) -> None:
    """
    Display information message.
    """

    st.info(message)


# ==============================================================================
# Divider
# ==============================================================================

def divider() -> None:
    """
    Display a horizontal divider.
    """

    st.markdown("---")


# ==============================================================================
# Metric Cards
# ==============================================================================

def metric_row(
    metrics: list[tuple[str, str]]
) -> None:
    """
    Display KPI metric cards.

    Example
    -------
    metric_row(
        [
            ("Current Model", "Version 1"),
            ("Pipeline", "Healthy"),
            ("AI Diagnosis", "Ready"),
            ("Self-Healing", "Enabled")
        ]
    )
    """

    if not metrics:

        return

    columns = st.columns(len(metrics))

    for column, (label, value) in zip(columns, metrics):

        with column:

            st.metric(

                label=label,

                value=value

            )


# ==============================================================================
# Workflow Progress
# ==============================================================================

def workflow_progress(
    stage: str
) -> None:
    """
    Display current workflow progress.
    """

    progress = STAGE_PROGRESS.get(

        stage,

        0

    )

    st.progress(progress)

    st.caption(

        f"Current Workflow Stage : {stage.replace('_', ' ').title()}"

    )


# ==============================================================================
# Footer
# ==============================================================================

def page_footer(
    version: str = "Version 1.0"
) -> None:
    """
    Display common footer.
    """

    divider()

    st.caption(

        f"Self-Healing Agentic AI ML Pipeline | {version}"

    )