"""
===============================================================================
Project : Self-Healing Agentic AI ML Pipeline

File    : evaluator.py

Purpose :
Evaluate Machine Learning Model Performance

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

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

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

logger = logging.getLogger("ModelEvaluator")

logger.setLevel(config.LOG_LEVEL)

formatter = logging.Formatter(config.LOG_FORMAT)

console_handler = logging.StreamHandler(sys.stdout)

console_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(console_handler)

# ==============================================================================
# Model Evaluator
# ==============================================================================


class ModelEvaluator:
    """
    Evaluate trained ML models.

    Responsibilities
    ----------------
    1. Calculate MAE
    2. Calculate RMSE
    3. Calculate R²
    4. Return evaluation metadata
    """

    # -------------------------------------------------------------------------

    def __init__(self):

        pass

    # -------------------------------------------------------------------------

    def calculate_metrics(
        self,
        y_true,
        y_pred
    ) -> Dict[str, float]:
        """
        Calculate regression metrics.

        Parameters
        ----------
        y_true

        y_pred

        Returns
        -------
        Dict
        """

        logger.info("Calculating model metrics...")

        mae = mean_absolute_error(
            y_true,
            y_pred
        )

        rmse = np.sqrt(

            mean_squared_error(
                y_true,
                y_pred
            )

        )

        r2 = r2_score(

            y_true,

            y_pred

        )

        logger.info("Metric calculation completed.")

        return {

            "mae": round(float(mae), 4),

            "rmse": round(float(rmse), 4),

            "r2": round(float(r2), 4)

        }

    # -------------------------------------------------------------------------

    def evaluate(
        self,
        training_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Evaluate training output.

        Parameters
        ----------
        training_result

        Returns
        -------
        Dict
        """

        logger.info("=" * 60)
        logger.info("Starting Model Evaluation")
        logger.info("=" * 60)

        required_keys = [

            "y_test",

            "y_pred"

        ]

        for key in required_keys:

            if key not in training_result:

                raise ValueError(

                    f"{key} missing from training result."

                )

        y_test = training_result["y_test"]

        y_pred = training_result["y_pred"]

        metrics = self.calculate_metrics(

            y_test,

            y_pred

        )

        evaluation_result = {

            **metrics,

            "sample_count": len(y_test),

            "evaluation_time": datetime.now().isoformat()

        }

        logger.info("Evaluation completed successfully.")

        return evaluation_result
    
    # -------------------------------------------------------------------------

    def print_summary(
        self,
        evaluation_result: Dict[str, Any]
    ):
        """
        Print evaluation summary.

        Parameters
        ----------
        evaluation_result : Dict
        """

        print()

        print("=" * 70)
        print("MODEL EVALUATION SUMMARY")
        print("=" * 70)

        print(f"MAE               : {evaluation_result['mae']:.4f}")
        print(f"RMSE              : {evaluation_result['rmse']:.4f}")
        print(f"R² Score          : {evaluation_result['r2']:.4f}")
        print(f"Sample Count      : {evaluation_result['sample_count']}")
        print(f"Evaluation Time   : {evaluation_result['evaluation_time']}")

        print("=" * 70)

    # -------------------------------------------------------------------------

    def validate_results(
        self,
        evaluation_result: Dict[str, Any]
    ) -> bool:
        """
        Validate evaluation results.

        Parameters
        ----------
        evaluation_result : Dict

        Returns
        -------
        bool
        """

        logger.info("Validating evaluation results...")

        required_keys = [

            "mae",

            "rmse",

            "r2",

            "sample_count",

            "evaluation_time"

        ]

        missing = [

            key

            for key in required_keys

            if key not in evaluation_result

        ]

        if missing:

            raise ValueError(

                f"Missing evaluation fields : {missing}"

            )

        if evaluation_result["sample_count"] <= 0:

            raise ValueError(

                "Sample count must be greater than zero."

            )

        logger.info(

            "Evaluation validation successful."

        )

        return True
    
# ==============================================================================
# Standalone Testing
# ==============================================================================

if __name__ == "__main__":

    from data.generator import SalesDataGenerator
    from ml.feature_engineering import FeatureEngineer
    from ml.trainer import ModelTrainer

    print("=" * 70)
    print("MODEL EVALUATOR TEST")
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

        processed_df, _ = engineer.prepare_features(

            raw_df

        )

        # ---------------------------------------------------------
        # Train Model
        # ---------------------------------------------------------

        trainer = ModelTrainer()

        training_result = trainer.train(

            processed_df

        )

        # ---------------------------------------------------------
        # Evaluate Model
        # ---------------------------------------------------------

        evaluator = ModelEvaluator()

        evaluation_result = evaluator.evaluate(

            training_result

        )

        evaluator.validate_results(

            evaluation_result

        )

        evaluator.print_summary(

            evaluation_result

        )

        print()

        print("=" * 70)
        print("MODEL EVALUATOR TEST PASSED")
        print("=" * 70)

    except Exception as error:

        logger.exception(error)

        print()

        print("=" * 70)
        print("MODEL EVALUATOR TEST FAILED")
        print("=" * 70)

        print(error)