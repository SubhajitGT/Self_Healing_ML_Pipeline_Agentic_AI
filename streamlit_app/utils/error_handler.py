"""
===============================================================================
Project : Self-Healing Agentic AI ML Pipeline

File    : error_handler.py

Purpose :
Centralized exception handling, logging and execution wrappers.

Author  : ChatGPT
===============================================================================
"""

from __future__ import annotations

import logging
import traceback
from typing import Any

import streamlit as st


# ==============================================================================
# Logger
# ==============================================================================

logger = logging.getLogger(__name__)


# ==============================================================================
# User Friendly Error Messages
# ==============================================================================

ERROR_MESSAGES = {

    FileNotFoundError:
        "Required file not found.",

    PermissionError:
        "Permission denied while accessing the file.",

    ValueError:
        "Invalid input provided.",

    KeyError:
        "Required information is missing.",

    RuntimeError:
        "Unexpected runtime error occurred."

}


# ==============================================================================
# Get Friendly Message
# ==============================================================================

def get_error_message(
    exception: Exception
) -> str:

    return ERROR_MESSAGES.get(

        type(exception),

        "An unexpected error occurred."

    )


# ==============================================================================
# Log Exception
# ==============================================================================

def log_exception(
    exception: Exception
) -> None:

    logger.exception(

        str(exception)

    )


# ==============================================================================
# Show Error
# ==============================================================================

def show_error(
    exception: Exception,
    show_traceback: bool = False
) -> None:

    st.error(

        get_error_message(exception)

    )

    if show_traceback:

        st.code(

            traceback.format_exc(),

            language="text"

        )


# ==============================================================================
# Execute Safely
# ==============================================================================

def safe_execute(
    func,
    *args,
    **kwargs
) -> Any:

    try:

        return func(

            *args,

            **kwargs

        )

    except Exception as exception:

        log_exception(

            exception

        )

        show_error(

            exception

        )

        return None