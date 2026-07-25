"""
===============================================================================
Project : Self-Healing Agentic AI ML Pipeline

File    : retraining_engine.py

Purpose :
Train and evaluate a candidate model for self-healing.

Author  : ChatGPT
===============================================================================
"""

from __future__ import annotations

import sys
import logging
import time
from pathlib import Path
from typing import Dict

import pandas as pd

# ==============================================================================
# Add Project Root
# ==============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ==============================================================================

import config

from ml.feature_engineering import FeatureEngineer
from ml.trainer import ModelTrainer
from ml.evaluator import ModelEvaluator

# ==============================================================================
# Logging
# ==============================================================================

logger = logging.getLogger("RetrainingEngine")

logger.setLevel(config.LOG_LEVEL)

formatter = logging.Formatter(config.LOG_FORMAT)

console_handler = logging.StreamHandler(sys.stdout)

console_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(console_handler)

# ==============================================================================
# Retraining Engine
# ==============================================================================


class RetrainingEngine:
    """
    Retraining Engine.

    Responsibilities
    ----------------
    1. Prepare dataset
    2. Train candidate model
    3. Evaluate candidate model
    """

    # -------------------------------------------------------------------------

    def __init__(self):

        self.feature_engineer = FeatureEngineer()

        self.trainer = ModelTrainer()

        self.evaluator = ModelEvaluator()

    # -------------------------------------------------------------------------

    def prepare_dataset(
        self,
        dataframe: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Prepare dataset for retraining.

        Parameters
        ----------
        dataframe : pd.DataFrame

        Returns
        -------
        pd.DataFrame
        """

        logger.info("=" * 60)
        logger.info("Preparing Dataset")
        logger.info("=" * 60)

        processed_df, metadata = (

            self.feature_engineer.prepare_features(

                dataframe

            )

        )

        logger.info(

            "Rows      : %d",

            len(processed_df)

        )

        logger.info(

            "Columns   : %d",

            len(processed_df.columns)

        )

        logger.info(

            "Dataset preparation completed."

        )

        return processed_df

    # -------------------------------------------------------------------------

    def train_candidate_model(
        self,
        processed_df: pd.DataFrame
    ) -> Dict:
        """
        Train a candidate model.

        Parameters
        ----------
        processed_df : pd.DataFrame

        Returns
        -------
        Dict
        """

        logger.info("=" * 60)
        logger.info("Training Candidate Model")
        logger.info("=" * 60)

        training_result = self.trainer.train(

            processed_df

        )

        logger.info(

            "Candidate model training completed."

        )

        return training_result

    # -------------------------------------------------------------------------

    def evaluate_candidate(
        self,
        training_result: Dict
    ) -> Dict:
        """
        Evaluate candidate model.

        Parameters
        ----------
        training_result : Dict

        Returns
        -------
        Dict
        """

        logger.info("=" * 60)
        logger.info("Evaluating Candidate Model")
        logger.info("=" * 60)

        model = training_result["model"]

        X_test = training_result["X_test"]

        y_test = training_result["y_test"]

        metrics = self.evaluator.evaluate(

            model,

            X_test,

            y_test

        )

        logger.info(

            "Candidate evaluation completed."

        )

        return metrics
    
    # -------------------------------------------------------------------------

    def retrain(
        self,
        dataframe: pd.DataFrame
    ) -> Dict:
        """
        Complete retraining workflow.

        Parameters
        ----------
        dataframe : pd.DataFrame

        Returns
        -------
        Dict
        """

        logger.info("=" * 60)
        logger.info("Starting Self-Healing Retraining")
        logger.info("=" * 60)

        start_time = time.time()

        # ---------------------------------------------------------
        # Prepare Dataset
        # ---------------------------------------------------------

        processed_df = self.prepare_dataset(

            dataframe

        )

        # ---------------------------------------------------------
        # Train Candidate
        # ---------------------------------------------------------

        training_result = self.train_candidate_model(

            processed_df

        )

        # ---------------------------------------------------------
        # Evaluate Candidate
        # ---------------------------------------------------------

        metrics = self.evaluate_candidate(

            training_result

        )

        # ---------------------------------------------------------
        # Training Summary
        # ---------------------------------------------------------

        training_time = round(

            time.time() - start_time,

            2

        )

        summary = {

            "rows":

                len(processed_df),

            "features":

                processed_df.shape[1] - 1,

            "training_time_seconds":

                training_time

        }

        logger.info("=" * 60)
        logger.info("Retraining Completed")
        logger.info("=" * 60)

        return {

            "candidate_model":

                training_result["model"],

            "candidate_metrics":

                metrics,

            "training_result":

                training_result,

            "training_summary":

                summary

        }
    
# ==============================================================================
# Standalone Testing
# ==============================================================================

if __name__ == "__main__":

    from data.generator import SalesDataGenerator

    print("=" * 70)
    print("RETRAINING ENGINE TEST")
    print("=" * 70)

    try:

        # ---------------------------------------------------------
        # Generate Dataset
        # ---------------------------------------------------------

        generator = SalesDataGenerator(

            rows=1000

        )

        dataframe = generator.generate_dataset()

        # ---------------------------------------------------------
        # Retraining
        # ---------------------------------------------------------

        engine = RetrainingEngine()

        result = engine.retrain(

            dataframe

        )

        print()

        print("=" * 70)
        print("TRAINING SUMMARY")
        print("=" * 70)

        summary = result["training_summary"]

        print(

            "Rows               :",

            summary["rows"]

        )

        print(

            "Features           :",

            summary["features"]

        )

        print(

            "Training Time (s)  :",

            summary["training_time_seconds"]

        )

        print()

        print("=" * 70)
        print("CANDIDATE METRICS")
        print("=" * 70)

        metrics = result["candidate_metrics"]

        print(

            "MAE   :",

            round(metrics["mae"], 4)

        )

        print(

            "RMSE  :",

            round(metrics["rmse"], 4)

        )

        print(

            "R²    :",

            round(metrics["r2"], 4)

        )

        print()

        print("=" * 70)
        print("RETRAINING ENGINE TEST PASSED")
        print("=" * 70)

    except Exception as error:

        logger.exception(error)

        print()

        print("=" * 70)
        print("RETRAINING ENGINE TEST FAILED")
        print("=" * 70)

        print(error)