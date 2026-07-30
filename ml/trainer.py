"""
===============================================================================
Project : Self-Healing Agentic AI ML Pipeline

File    : trainer.py

Purpose :
Train Production ML Pipeline using sklearn Pipeline.

Author  : ChatGPT
===============================================================================
"""

from __future__ import annotations

import sys
import logging
from pathlib import Path
from typing import Dict, List

import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from datetime import datetime

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
    Production Model Trainer.

    Responsibilities
    ----------------
    1. Split train/test data
    2. Build preprocessing pipeline
    3. Train ML Pipeline
    4. Validate pipeline
    5. Return training artefacts
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
        Split dataframe into train/test.
        """

        logger.info("=" * 60)
        logger.info("Preparing Train/Test Split")
        logger.info("=" * 60)

        if self.target_column not in dataframe.columns:

            raise ValueError(

                f"Target column '{self.target_column}' not found."

            )

        X = dataframe.drop(

            columns=[self.target_column]

        )

        y = dataframe[self.target_column]

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

            "feature_columns": X.columns.tolist()

        }

    # -------------------------------------------------------------------------

    def build_pipeline(
        self,
        X_train: pd.DataFrame
    ) -> Pipeline:
        """
        Build sklearn Pipeline.
        """

        logger.info(

            "Building preprocessing pipeline..."

        )

        categorical_columns = X_train.select_dtypes(

            include=[

                "object",

                "category",

                "bool"

            ]

        ).columns.tolist()

        numeric_columns = [

            column

            for column in X_train.columns

            if column not in categorical_columns

        ]

        logger.info(

            "Categorical Columns : %s",

            categorical_columns

        )

        logger.info(

            "Numeric Columns : %s",

            numeric_columns

        )

        preprocessor = ColumnTransformer(

            transformers=[

                (

                    "numeric",

                    Pipeline(

                        steps=[

                            (

                                "imputer",

                                SimpleImputer(

                                    strategy="median"

                                )

                            )

                        ]

                    ),

                    numeric_columns

                ),

                (

                    "categorical",

                    Pipeline(

                        steps=[

                            (

                                "imputer",

                                SimpleImputer(

                                    strategy="most_frequent"

                                )

                            ),

                            (

                                "encoder",

                                OneHotEncoder(

                                    handle_unknown="ignore"

                                )

                            )

                        ]

                    ),

                    categorical_columns

                )

            ],

            remainder="drop"

        )

        pipeline = Pipeline(

            steps=[

                (

                    "preprocessor",

                    preprocessor

                ),

                (

                    "model",

                    GradientBoostingRegressor(

                        n_estimators=config.N_ESTIMATORS,

                        learning_rate=config.LEARNING_RATE,

                        max_depth=config.MAX_DEPTH,

                        random_state=self.random_seed

                    )

                )

            ]

        )

        logger.info(

            "Pipeline created successfully."

        )

        return pipeline
    
        # -------------------------------------------------------------------------

    def train(
        self,
        dataframe: pd.DataFrame
    ) -> Dict:
        """
        Train complete ML Pipeline.

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
        # Split Dataset
        # ---------------------------------------------------------

        split_result = self.split_data(

            dataframe

        )

        X_train = split_result["X_train"]

        X_test = split_result["X_test"]

        y_train = split_result["y_train"]

        y_test = split_result["y_test"]

        feature_columns = split_result["feature_columns"]

        # ---------------------------------------------------------
        # Build Pipeline
        # ---------------------------------------------------------

        pipeline = self.build_pipeline(

            X_train

        )

        logger.info(

            "Training ML Pipeline..."

        )
        print("\n==================== DTYPES ====================")
        print(X_train.dtypes)
        print("================================================\n")


        pipeline.fit(

            X_train,

            y_train

        )

        logger.info(

            "Training completed."

        )

        # ---------------------------------------------------------
        # Prediction
        # ---------------------------------------------------------

        logger.info(

            "Generating predictions..."

        )

        y_pred = pipeline.predict(

            X_test

        )

        logger.info(

            "Prediction completed."

        )

        # ---------------------------------------------------------
        # Metadata
        # ---------------------------------------------------------

        metadata = {

            "training_rows":

                len(X_train),

            "testing_rows":

                len(X_test),

            "feature_count":

                len(feature_columns),

            "feature_columns":

                feature_columns,

            "target_column":

                self.target_column,

            "model_name":

                config.MODEL_NAME,
            
            "model_version":
    config.DEFAULT_MODEL_VERSION,

            "model_file":
    config.MODEL_FILE_NAME,
    
            "training_timestamp":
    datetime.now().isoformat(),

            "hyperparameters": {

                "n_estimators":

                    config.N_ESTIMATORS,

                "learning_rate":

                    config.LEARNING_RATE,

                "max_depth":

                    config.MAX_DEPTH,

                "test_size":

                    config.TEST_SIZE,

                "random_seed":

                    config.RANDOM_SEED

            }

        }

        training_result = {

            "model":

                pipeline,

            "X_train":

                X_train,

            "X_test":

                X_test,

            "y_train":

                y_train,

            "y_test":

                y_test,

            "y_pred":

                y_pred,

            "feature_columns":

                feature_columns,

            "metadata":

                metadata

        }

        self.validate_trained_model(

            training_result

        )

        logger.info("=" * 60)
        logger.info("Training Completed Successfully")
        logger.info("=" * 60)

        return training_result

    # -------------------------------------------------------------------------

    def validate_trained_model(
        self,
        training_result: Dict
    ) -> bool:
        """
        Validate training result.
        """

        logger.info(

            "Validating trained pipeline..."

        )

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

                f"Missing keys : {missing}"

            )

        if not isinstance(

            training_result["model"],

            Pipeline

        ):

            raise TypeError(

                "Returned object is not a sklearn Pipeline."

            )

        if len(

            training_result["X_test"]

        ) != len(

            training_result["y_pred"]

        ):

            raise ValueError(

                "Prediction count mismatch."

            )

        logger.info(

            "Pipeline validation successful."

        )

        return True

    # -------------------------------------------------------------------------

    def print_summary(
        self,
        training_result: Dict
    ) -> None:
        """
        Print training summary.
        """

        metadata = training_result["metadata"]

        print()

        print("=" * 70)
        print("MODEL TRAINING SUMMARY")
        print("=" * 70)

        print(

            "Model Name        :",

            metadata["model_name"]

        )

        print(

            "Training Rows     :",

            metadata["training_rows"]

        )

        print(

            "Testing Rows      :",

            metadata["testing_rows"]

        )

        print(

            "Feature Count     :",

            metadata["feature_count"]

        )

        print(

            "Target Column     :",

            metadata["target_column"]

        )

        print("=" * 70)

# ==============================================================================
# Standalone Testing
# ==============================================================================

if __name__ == "__main__":

    from data.generator import SalesDataGenerator
    from ml.evaluator import ModelEvaluator

    print("=" * 70)
    print("MODEL TRAINER TEST")
    print("=" * 70)

    try:

        # ---------------------------------------------------------
        # Generate Dataset
        # ---------------------------------------------------------

        generator = SalesDataGenerator(

            rows=1000

        )

        dataframe = generator.generate_dataset()

        print()

        print("Dataset Generated Successfully")

        print("Rows :", len(dataframe))

        print("Columns :", len(dataframe.columns))

        # ---------------------------------------------------------
        # Feature Engineering
        # ---------------------------------------------------------

        from ml.feature_engineering import FeatureEngineer

        engineer = FeatureEngineer()

        processed_df, _ = engineer.prepare_features(

            dataframe

        )
        # ---------------------------------------------------------
        # Train Model
        # ---------------------------------------------------------

        trainer = ModelTrainer()

        training_result = trainer.train(

            processed_df

        )

        trainer.print_summary(

            training_result

        )

        # ---------------------------------------------------------
        # Evaluate
        # ---------------------------------------------------------

        evaluator = ModelEvaluator()

        evaluation_result = evaluator.evaluate(

            training_result

        )

        evaluator.print_summary(

            evaluation_result

        )

        print()

        print("=" * 70)
        print("MODEL TRAINER TEST PASSED")
        print("=" * 70)

    except Exception as error:

        logger.exception(error)

        print()

        print("=" * 70)
        print("MODEL TRAINER TEST FAILED")
        print("=" * 70)

        print(error)