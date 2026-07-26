"""
===============================================================================
Project : Self-Healing Agentic AI ML Pipeline

File    : 4_Model_Prediction.py

Purpose :
Generate predictions using the production model.

Author  : ChatGPT
===============================================================================
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st
import traceback

# ==============================================================================
# Add Project Root
# ==============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ==============================================================================

from ml.feature_engineering import FeatureEngineer
from ml.model_manager import ModelManager
from ml.predictor import Predictor

from utils.session import initialize_session_state

initialize_session_state()

import sklearn
st.write(sklearn.__version__)
# ==============================================================================
# Page
# ==============================================================================

st.set_page_config(

    page_title="Prediction",

    page_icon="📈",

    layout="wide"

)

st.title("📈 Model Prediction")

st.markdown("---")

# ==============================================================================
# Dataset Check
# ==============================================================================

dataframe = st.session_state.get(

    "uploaded_dataframe"

)

if dataframe is None:

    st.warning(

        "Please upload a dataset first."

    )

    st.stop()

validation_report = st.session_state.get("validation_report")

if validation_report is None:

    st.warning(
        "Please run Data Validation before Prediction."
    )

    st.stop()

status = str(validation_report.get("status", "")).upper()

if status != "PASS":

    st.error(
        "Prediction is disabled because the uploaded dataset failed validation."
    )

    st.info(
        "Please upload a valid dataset or correct the validation errors."
    )

    st.stop()

# ==============================================================================
# Prediction
# ==============================================================================

if st.button(

    "Generate Predictions",

    use_container_width=True

):

    with st.spinner(

        "Generating predictions..."

    ):

        # ----------------------------------------------------------
        # Feature Engineering
        # ----------------------------------------------------------

        try:

            engineer = FeatureEngineer()

            processed_df, _ = engineer.prepare_features(

            dataframe.copy()

        )

        # ----------------------------------------------------------
        # Remove Target if Present
        # ----------------------------------------------------------

            target = getattr(

            engineer,

            "target_column",

            "sales"

        )

            if target in processed_df.columns:

                processed_df = processed_df.drop(

                columns=[target]

            )

        # ----------------------------------------------------------
        # Prediction
        # ----------------------------------------------------------

            predictor = Predictor()

            result = predictor.predict_using_saved_model(

            processed_df,

            version=1

        )

        except Exception:

            st.code(traceback.format_exc())

            st.stop()
        prediction_df = dataframe.copy()

        prediction_df["Prediction"] = result[

            "predictions"

        ]

        st.session_state.prediction_result = {

            "prediction_df": prediction_df,

            "metadata": result

        }

    st.success(

        "Prediction completed successfully."

    )

# ==============================================================================
# Results
# ==============================================================================

prediction_result = st.session_state.get(

    "prediction_result"

)

if prediction_result is not None:

    prediction_df = prediction_result[

        "prediction_df"

    ]

    metadata = prediction_result[

        "metadata"

    ]

    st.subheader(

        "Prediction Summary"

    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(

            "Rows",

            len(prediction_df)

        )

    with col2:

        st.metric(

            "Predictions",

            metadata["prediction_count"]

        )

    with col3:

        st.metric(

            "Model Version",

            metadata["model_version"]

        )

    st.markdown("---")

    st.subheader(

        "Prediction Results"

    )

    st.dataframe(

        prediction_df,

        use_container_width=True

    )

    csv = prediction_df.to_csv(

        index=False

    ).encode("utf-8")

    st.download_button(

        "Download Predictions",

        data=csv,

        file_name="predictions.csv",

        mime="text/csv"

    )