"""
===============================================================================
Project : Self-Healing Agentic AI ML Pipeline

File    : model_manager.py

Purpose :
Save and Load Machine Learning Models

Author  : ChatGPT
===============================================================================
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from datetime import datetime

import joblib
from sklearn.pipeline import Pipeline
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

logger = logging.getLogger("ModelManager")

logger.setLevel(config.LOG_LEVEL)

formatter = logging.Formatter(config.LOG_FORMAT)

console_handler = logging.StreamHandler(sys.stdout)

console_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(console_handler)

# ==============================================================================
# Model Manager
# ==============================================================================


class ModelManager:
    """
    Save and Load trained ML models.
    """

    # -------------------------------------------------------------------------

    def __init__(self):

        self.model_directory = config.SAVED_MODEL_DIR

        self.model_directory.mkdir(
            parents=True,
            exist_ok=True
        )

    # -------------------------------------------------------------------------

    def save_model(
        self,
        model,
        version: int = 1
    ) -> Path:
        """
        Save trained model.

        Parameters
        ----------
        model

        version : int

        Returns
        -------
        Path
        """

        model_name = f"sales_forecaster_v{version}.pkl"

        model_path = self.model_directory / model_name

        logger.info(
            "Saving model : %s",
            model_name
        )
        if not isinstance(model, Pipeline):

            raise TypeError(

        "Expected a sklearn Pipeline."

        )

        joblib.dump(

            model,

            model_path

        )

        logger.info(
            "Model saved successfully."
        )

        return model_path

    # -------------------------------------------------------------------------

    def load_model(
        self,
        version: int = None
    ):
        """
        Load saved model.

        Parameters
        ----------
        version : int

        Returns
        -------
        Trained Model
        """

        if version is None:

            version = 1

        model_name = f"sales_forecaster_v{version}.pkl"

        model_path = self.model_directory / model_name

        if not model_path.exists():

            raise FileNotFoundError(

                f"Model not found : {model_path}"

            )

        logger.info(
            "Loading model : %s",
            model_name
        )

        model = joblib.load(

            model_path

        )

        logger.info(
            "Model loaded successfully."
        )

        return model
    
    # -------------------------------------------------------------------------

    def list_models(self):
        """
        List all saved models.

        Returns
        -------
        list
            List of model filenames.
        """

        models = sorted(

            self.model_directory.glob("*.pkl")

        )

        logger.info(

            "Found %d model(s).",

            len(models)

        )

        return models
    
    # -------------------------------------------------------------------------

    def get_latest_model(self):
        """
        Return latest saved model.

        Returns
        -------
        Path
        """

        models = self.list_models()

        if not models:

            raise FileNotFoundError(

                "No saved models found."

            )

        latest_model = max(

            models,

            key=lambda file: file.stat().st_mtime

        )

        logger.info(

            "Latest Model : %s",

            latest_model.name

        )

        return latest_model
    
    # -------------------------------------------------------------------------

    def delete_model(
        self,
        version: int
    ):
        """
        Delete a saved model.

        Parameters
        ----------
        version : int
        """

        model_name = f"sales_forecaster_v{version}.pkl"

        model_path = self.model_directory / model_name

        if not model_path.exists():

            raise FileNotFoundError(

                f"{model_name} not found."

            )

        model_path.unlink()

        logger.info(

            "%s deleted successfully.",

            model_name

        )

# ==============================================================================
# Standalone Testing
# ==============================================================================

if __name__ == "__main__":

    from data.generator import SalesDataGenerator
    from ml.feature_engineering import FeatureEngineer
    from ml.trainer import ModelTrainer

    print("=" * 70)
    print("MODEL MANAGER TEST")
    print("=" * 70)

    try:

        # ---------------------------------------------------------
        # Generate Dataset
        # ---------------------------------------------------------

        generator = SalesDataGenerator(

            rows=1000

        )

        raw_df = generator.generate_dataset()

        # ---------------------------------------------------------
        # Feature Engineering
        # ---------------------------------------------------------

        engineer = FeatureEngineer()

        processed_df, _ = engineer.prepare_features(

            raw_df

        )

        # ---------------------------------------------------------
        # Train Model
        # ---------------------------------------------------------

        trainer = ModelTrainer()

        result = trainer.train(

            processed_df

        )

        model = result["model"]

        # ---------------------------------------------------------
        # Save Model
        # ---------------------------------------------------------

        manager = ModelManager()

        saved_path = manager.save_model(

            model,

            version=1

        )

        print()

        print("=" * 70)
        print("MODEL SAVED")
        print("=" * 70)

        print(saved_path)

        # ---------------------------------------------------------
        # Load Model
        # ---------------------------------------------------------

        loaded_model = manager.load_model(

            version=1

        )

        print()

        print("=" * 70)
        print("MODEL LOADED")
        print("=" * 70)

        print(type(loaded_model).__name__)

        # ---------------------------------------------------------
        # List Models
        # ---------------------------------------------------------

        print()

        print("=" * 70)
        print("AVAILABLE MODELS")
        print("=" * 70)

        models = manager.list_models()

        for model_file in models:

            print(model_file.name)

        # ---------------------------------------------------------
        # Latest Model
        # ---------------------------------------------------------

        latest = manager.get_latest_model()

        print()

        print("=" * 70)
        print("LATEST MODEL")
        print("=" * 70)

        print(latest.name)

        print()

        print("=" * 70)
        print("MODEL MANAGER TEST PASSED")
        print("=" * 70)

    except Exception as error:

        logger.exception(error)

        print()

        print("=" * 70)
        print("MODEL MANAGER TEST FAILED")
        print("=" * 70)

        print(error)