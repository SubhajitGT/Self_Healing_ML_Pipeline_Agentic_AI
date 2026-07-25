import streamlit as st


def initialize_session_state():
    """Initialize all session state variables."""

    defaults = {
        "uploaded_dataframe": None,
        "validation_report": None,
        "prediction_result": None,
        "drift_report": None,
        "performance_report": None,
        "ai_report": None,
        "self_healing_report": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value