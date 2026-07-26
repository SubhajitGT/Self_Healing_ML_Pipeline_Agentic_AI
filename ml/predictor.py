"""
===============================================================================
Project : Self-Healing Agentic AI ML Pipeline

File    : predictor.py

Purpose :
Generate predictions using trained ML models.

Author  : ChatGPT
===============================================================================
"""

from __future__ import annotations

import sys
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

import numpy as np
import pandas as pd

# ==============================================================================
# Add Project Root
# ==============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ==============================================================================

import config

# ==============================================================================
# Logging
# ==============================================================================

logger = logging.getLogger("Predictor")

logger.setLevel(config.LOG_LEVEL)

formatter = logging.Formatter(config.LOG_FORMAT)

console_handler = logging.StreamHandler(sys.stdout)

console_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(console_handler)


# ==============================================================================
# Predictor
# ==============================================================================

class Predictor:
    """
    Prediction module.

    Responsibilities
    ----------------
    1. Predict using trained model
    2. Predict single record
    3. Return prediction metadata
    """

    # -------------------------------------------------------------------------

    def __init__(self):

        self.target_column = config.TARGET_COLUMN

    # -------------------------------------------------------------------------

    def predict_dataframe(
        self,
        model,
        dataframe: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        Predict an entire dataframe.

        Parameters
        ----------
        model
            Trained sklearn model.

        dataframe : pd.DataFrame
            Feature dataframe only.

        Returns
        -------
        Dict
        """

        logger.info("=" * 60)
        logger.info("Starting Batch Prediction")
        logger.info("=" * 60)

        if dataframe.empty:

            raise ValueError(
                "Input dataframe is empty."
            )

        logger.info(
            "Prediction Rows : %d",
            len(dataframe)
        )

        predictions = model.predict(dataframe)

        logger.info(
            "Prediction completed successfully."
        )

        return {

            "predictions": predictions,

            "prediction_count": len(predictions),

            "prediction_time": datetime.now().isoformat()

        }

    # -------------------------------------------------------------------------

    def predict_record(
        self,
        model,
        record
    ) -> float:
        """
        Predict a single record.

        Parameters
        ----------
        model

        record :
            One row dataframe OR dictionary.

        Returns
        -------
        float
        """

        logger.info(
            "Predicting single record..."
        )

        # ---------------------------------------------------------
        # Dictionary
        # ---------------------------------------------------------

        if isinstance(record, dict):

            record = pd.DataFrame([record])

        # ---------------------------------------------------------
        # Series
        # ---------------------------------------------------------

        elif isinstance(record, pd.Series):

            record = record.to_frame().T

        # ---------------------------------------------------------
        # Validation
        # ---------------------------------------------------------

        if not isinstance(record, pd.DataFrame):

            raise TypeError(

                "Record must be dict, Series or DataFrame."

            )

        prediction = model.predict(record)[0]

        logger.info(
            "Prediction generated successfully."
        )

        return float(prediction)
    
    # -------------------------------------------------------------------------

    def validate_prediction_input(
        self,
        dataframe: pd.DataFrame
    ) -> bool:
        """
        Validate prediction input dataframe.

        Parameters
        ----------
        dataframe : pd.DataFrame

        Returns
        -------
        bool
        """

        logger.info("Validating prediction input...")

        if dataframe is None:

            raise ValueError(
                "Prediction dataframe cannot be None."
            )

        if dataframe.empty:

            raise ValueError(
                "Prediction dataframe is empty."
            )

        if self.target_column in dataframe.columns:

            logger.warning(
                "Target column '%s' found in prediction dataframe. Removing it.",
                self.target_column
            )

            dataframe.drop(
                columns=[self.target_column],
                inplace=True,
                errors="ignore"
            )

        logger.info("Prediction input validation successful.")

        return True
    
    # -------------------------------------------------------------------------

    def predict_using_saved_model(
        self,
        dataframe: pd.DataFrame,
        version: int = 1
    ) -> Dict[str, Any]:
        """
        Load a saved model and predict.

        Parameters
        ----------
        dataframe : pd.DataFrame

        version : int

        Returns
        -------
        Dict
        """

        logger.info("=" * 60)
        logger.info("Prediction Using Saved Model")
        logger.info("=" * 60)

        from ml.model_manager import ModelManager

        self.validate_prediction_input(dataframe)

        manager = ModelManager()

        print("=" * 80)
        print("Loading model...")
        print("Version :", version)
        model = manager.load_model(version)
        print("Loaded :", type(model))
        print("=" * 80)

        prediction_result = self.predict_dataframe(

            model,

            dataframe

        )

        prediction_result["model_version"] = version

        return prediction_result
    
# ==============================================================================
# Standalone Testing
# ==============================================================================

if __name__ == "__main__":

    from data.generator import SalesDataGenerator
    from ml.feature_engineering import FeatureEngineer
    from ml.trainer import ModelTrainer
    from ml.model_manager import ModelManager

    print("=" * 70)
    print("PREDICTOR TEST")
    print("=" * 70)

    try:

        # ---------------------------------------------------------
        # Generate Dataset
        # ---------------------------------------------------------

        generator = SalesDataGenerator(rows=1000)

        raw_df = generator.generate_dataset()

        # ---------------------------------------------------------
        # Feature Engineering
        # ---------------------------------------------------------

        engineer = FeatureEngineer()

        processed_df, _ = engineer.prepare_features(raw_df)

        # ---------------------------------------------------------
        # Train Model
        # ---------------------------------------------------------

        trainer = ModelTrainer()

        training_result = trainer.train(processed_df)

        model = training_result["model"]

        X_test = training_result["X_test"]

        # ---------------------------------------------------------
        # Save Model
        # ---------------------------------------------------------

        manager = ModelManager()

        manager.save_model(

            model,

            version=1

        )

        # ---------------------------------------------------------
        # Predictor
        # ---------------------------------------------------------

        predictor = Predictor()

        prediction_result = predictor.predict_using_saved_model(

            X_test,

            version=1

        )

        print()

        print("=" * 70)
        print("PREDICTION SUMMARY")
        print("=" * 70)

        print(
            "Prediction Count :",
            prediction_result["prediction_count"]
        )

        print(
            "Prediction Time  :",
            prediction_result["prediction_time"]
        )

        print(
            "Model Version    :",
            prediction_result["model_version"]
        )

        print()

        print("=" * 70)
        print("FIRST 10 PREDICTIONS")
        print("=" * 70)

        for prediction in prediction_result["predictions"][:10]:

            print(round(float(prediction), 2))

        print()

        print("=" * 70)
        print("PREDICTOR TEST PASSED")
        print("=" * 70)

    except Exception as error:

        logger.exception(error)

        print()

        print("=" * 70)
        print("PREDICTOR TEST FAILED")
        print("=" * 70)

        print(error)