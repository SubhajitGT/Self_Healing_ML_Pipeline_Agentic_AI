"""
===============================================================================
Project : Self-Healing Agentic AI ML Pipeline

File    : trainer.py

Purpose :
Train Machine Learning model.

Author  : ChatGPT
===============================================================================
"""

from __future__ import annotations

import sys
import logging
from pathlib import Path
from typing import Dict

# ==============================================================================
# Add Project Root
# ==============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ==============================================================================

import pandas as pd

from sklearn.model_selection import train_test_split

import config

# ==============================================================================
# Logging
# ==============================================================================

logger = logging.getLogger("ModelTrainer")

logger.setLevel(config.LOG_LEVEL)

formatter = logging.Formatter(config.LOG_FORMAT)

console_handler = logging.StreamHandler(sys.stdout)

console_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(console_handler)


# ==============================================================================
# Model Trainer
# ==============================================================================

class ModelTrainer:
    """
    Train Machine Learning model.

    Responsibilities
    ----------------
    1. Split dataset
    2. Prepare feature matrix
    3. Prepare target vector
    4. Return train/test datasets

    Actual model training will be added in Phase 3.2A.2.
    """

    # -------------------------------------------------------------------------

    def __init__(self):

        self.target_column = config.TARGET_COLUMN

        self.test_size = config.TEST_SIZE

        self.random_seed = config.RANDOM_SEED

    # -------------------------------------------------------------------------

    def split_data(
        self,
        dataframe: pd.DataFrame
    ) -> Dict:
        """
        Split processed dataframe into
        training and testing datasets.

        Parameters
        ----------
        dataframe : pd.DataFrame

        Returns
        -------
        Dict
        """

        logger.info("Preparing train/test datasets...")

        if self.target_column not in dataframe.columns:

            raise ValueError(

                f"Target column '{self.target_column}' not found."

            )

        # -----------------------------------------------------
        # Separate Features and Target
        # -----------------------------------------------------

        X = dataframe.drop(

            columns=[self.target_column]

        )

        y = dataframe[

            self.target_column

        ]

        feature_columns = X.columns.tolist()

        # -----------------------------------------------------
        # Train/Test Split
        # -----------------------------------------------------

        X_train, X_test, y_train, y_test = train_test_split(

            X,

            y,

            test_size=self.test_size,

            random_state=self.random_seed,

            shuffle=True

        )

        logger.info(

            "Training rows : %d",

            len(X_train)

        )

        logger.info(

            "Testing rows : %d",

            len(X_test)

        )

        return {

            "X_train": X_train,

            "X_test": X_test,

            "y_train": y_train,

            "y_test": y_test,

            "feature_columns": feature_columns

        }
    
    # -------------------------------------------------------------------------

    def build_model(self):
        """
        Build the Machine Learning model.

        Returns
        -------
        GradientBoostingRegressor
        """

        logger.info("Building Gradient Boosting model...")

        from sklearn.ensemble import GradientBoostingRegressor

        model = GradientBoostingRegressor(

            n_estimators=config.N_ESTIMATORS,

            learning_rate=config.LEARNING_RATE,

            max_depth=config.MAX_DEPTH,

            random_state=self.random_seed

        )

        logger.info("Model created successfully.")

        return model

    # -------------------------------------------------------------------------

    def train(
        self,
        dataframe: pd.DataFrame
    ) -> Dict:
        """
        Train the Gradient Boosting model.

        Parameters
        ----------
        dataframe : pd.DataFrame

        Returns
        -------
        Dict
        """

        logger.info("=" * 60)
        logger.info("Starting Model Training")
        logger.info("=" * 60)

        # ---------------------------------------------------------
        # Split dataset
        # ---------------------------------------------------------

        split_result = self.split_data(dataframe)

        X_train = split_result["X_train"]

        X_test = split_result["X_test"]

        y_train = split_result["y_train"]

        y_test = split_result["y_test"]

        feature_columns = split_result["feature_columns"]

        # ---------------------------------------------------------
        # Build model
        # ---------------------------------------------------------

        model = self.build_model()

        # ---------------------------------------------------------
        # Train model
        # ---------------------------------------------------------

        logger.info("Training model...")

        model.fit(

            X_train,

            y_train

        )

        logger.info("Model training completed.")

        # ---------------------------------------------------------
        # Prediction
        # ---------------------------------------------------------

        logger.info("Generating predictions...")

        y_pred = model.predict(

            X_test

        )

        logger.info("Prediction completed.")

        # ---------------------------------------------------------
        # Training metadata
        # ---------------------------------------------------------

            # ---------------------------------------------------------
    # Training metadata
    # ---------------------------------------------------------

        training_metadata = {

        "training_rows": len(X_train),

        "testing_rows": len(X_test),

        "feature_count": len(feature_columns),

        "model_name": type(model).__name__,

        "target_column": self.target_column,

        "hyperparameters": {

            "n_estimators": config.N_ESTIMATORS,

            "learning_rate": config.LEARNING_RATE,

            "max_depth": config.MAX_DEPTH,

            "test_size": config.TEST_SIZE,

            "random_seed": config.RANDOM_SEED

        }

    }
        logger.info("=" * 60)
        logger.info("Training Completed")
        logger.info("=" * 60)

            # ---------------------------------------------------------
    # Validate Training Output
    # ---------------------------------------------------------

        result = {

            "model": model,

            "X_train": X_train,

            "X_test": X_test,

            "y_train": y_train,

            "y_test": y_test,

            "y_pred": y_pred,

            "feature_columns": feature_columns,

            "metadata": training_metadata

        }

        self.validate_trained_model(result)

        return result
    # -------------------------------------------------------------------------

    def validate_trained_model(
        self,
        training_result: Dict
    ) -> bool:
        """
        Validate that model training completed successfully.

        Parameters
        ----------
        training_result : Dict

        Returns
        -------
        bool
        """

        logger.info("Validating trained model...")

        required_keys = [

            "model",

            "X_train",

            "X_test",

            "y_train",

            "y_test",

            "y_pred",

            "feature_columns",

            "metadata"

        ]

        missing = [

            key

            for key in required_keys

            if key not in training_result

        ]

        if missing:

            raise ValueError(

                f"Training result missing keys : {missing}"

            )

        model = training_result["model"]

        if not hasattr(model, "predict"):

            raise TypeError(

                "Returned object is not a valid sklearn model."

            )

        if len(training_result["X_test"]) != len(training_result["y_pred"]):

            raise ValueError(

                "Prediction size does not match test dataset."

            )

        logger.info("Model validation successful.")

        return True

# ==============================================================================
# Standalone Testing
# ==============================================================================

if __name__ == "__main__":

    print("=" * 70)
    print("SELF-HEALING AGENTIC AI ML PIPELINE")
    print("MODEL TRAINER TEST")
    print("=" * 70)

    try:

        # ---------------------------------------------------------------------
        # Generate Sample Dataset
        # ---------------------------------------------------------------------

        logger.info("Generating sample dataset...")

        from data.generator import SalesDataGenerator
        from ml.feature_engineering import FeatureEngineer

        generator = SalesDataGenerator(rows=1000)

        raw_dataframe = generator.generate_dataset()

        logger.info(
            "Raw Dataset Shape : %s",
            raw_dataframe.shape
        )

        # ---------------------------------------------------------------------
        # Feature Engineering
        # ---------------------------------------------------------------------

        logger.info("Running Feature Engineering...")

        engineer = FeatureEngineer()

        processed_dataframe, feature_metadata = engineer.prepare_features(
            raw_dataframe
        )

        logger.info(
            "Processed Dataset Shape : %s",
            processed_dataframe.shape
        )

        # ---------------------------------------------------------------------
        # Model Training
        # ---------------------------------------------------------------------

        trainer = ModelTrainer()

        training_result = trainer.train(
            processed_dataframe
        )

        trainer.validate_trained_model(
            training_result
        )

        # ---------------------------------------------------------------------
        # Display Training Summary
        # ---------------------------------------------------------------------

        metadata = training_result["metadata"]

        print()
        print("=" * 70)
        print("TRAINING SUMMARY")
        print("=" * 70)

        print(f"Model Name           : {metadata['model_name']}")
        print(f"Target Column        : {metadata['target_column']}")
        print(f"Training Rows        : {metadata['training_rows']}")
        print(f"Testing Rows         : {metadata['testing_rows']}")
        print(f"Feature Count        : {metadata['feature_count']}")

        print()

        print("=" * 70)
        print("MODEL HYPERPARAMETERS")
        print("=" * 70)

        for key, value in metadata["hyperparameters"].items():

            print(f"{key:<20}: {value}")

        print()

        print("=" * 70)
        print("FEATURE ENGINEERING SUMMARY")
        print("=" * 70)

        for key, value in feature_metadata.items():

            print(f"{key:<30}: {value}")

        print()

        print("=" * 70)
        print("TRAIN / TEST SHAPES")
        print("=" * 70)

        print(
            "X_train :",
            training_result["X_train"].shape
        )

        print(
            "X_test  :",
            training_result["X_test"].shape
        )

        print(
            "y_train :",
            training_result["y_train"].shape
        )

        print(
            "y_test  :",
            training_result["y_test"].shape
        )

        print()

        print("=" * 70)
        print("FIRST FIVE FEATURES")
        print("=" * 70)

        for feature in training_result["feature_columns"][:5]:

            print(feature)

        print()

        print("=" * 70)
        print("MODEL OBJECT")
        print("=" * 70)

        print(training_result["model"])

        print()

        print("=" * 70)
        print("MODEL TRAINING COMPLETED SUCCESSFULLY")
        print("=" * 70)

    except Exception as error:

        logger.exception(error)

        print()

        print("=" * 70)
        print("MODEL TRAINING FAILED")
        print("=" * 70)

        print(error)