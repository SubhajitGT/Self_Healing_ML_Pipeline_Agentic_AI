"""
Workflow guards for Streamlit pages.
"""

import streamlit as st


def require_uploaded_dataset():

    dataframe = st.session_state.get(
        "uploaded_dataframe"
    )

    if dataframe is None:

        st.warning(
            "📂 Please upload a dataset first."
        )

        st.stop()

    return dataframe


def require_validation():

    report = st.session_state.get(
        "validation_report"
    )

    if report is None:

        st.warning(
            "✅ Please validate the dataset first."
        )

        st.stop()

    if report.get("status") != "PASS":

        st.error(
            "Dataset validation failed.\n\n"
            "Please upload a valid dataset before continuing."
        )

        st.stop()

    return report


def require_prediction():

    prediction = st.session_state.get(
        "prediction_result"
    )

    if prediction is None:

        st.warning(
            "📈 Please generate predictions first."
        )

        st.stop()

    return prediction


def require_monitoring():

    drift = st.session_state.get(
        "drift_report"
    )

    performance = st.session_state.get(
        "performance_report"
    )

    if drift is None or performance is None:

        st.warning(
            "📊 Please run Monitoring first."
        )

        st.stop()


def require_ai_report():

    report = st.session_state.get(
        "ai_report"
    )

    if report is None:

        st.warning(
            "🧠 Please run AI Diagnosis first."
        )

        st.stop()

    return report