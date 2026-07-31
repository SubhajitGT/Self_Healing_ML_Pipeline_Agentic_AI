"""
===============================================================================
Project : Self-Healing Agentic AI ML Pipeline

File    : performance_monitor.py

Purpose :
Monitor model performance degradation over time.

Author  : ChatGPT
===============================================================================
"""

from __future__ import annotations

import sys
import logging
from pathlib import Path
from typing import Dict
from ml.feature_engineering import FeatureEngineer

# ==============================================================================
# Add Project Root
# ==============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ==============================================================================

import config
from ml.model_manager import ModelManager
from ml.evaluator import ModelEvaluator

import pandas as pd

# ==============================================================================
# Logging
# ==============================================================================

logger = logging.getLogger("PerformanceMonitor")

logger.setLevel(config.LOG_LEVEL)

formatter = logging.Formatter(config.LOG_FORMAT)

console_handler = logging.StreamHandler(sys.stdout)

console_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(console_handler)

# ==============================================================================
# Performance Monitor
# ==============================================================================


class PerformanceMonitor:
    """
    Monitor model performance degradation.

    Responsibilities
    ----------------
    1. Compare evaluation metrics
    2. Calculate percentage changes
    3. Calculate model health score
    """

    # -------------------------------------------------------------------------

    def __init__(self):

        self.r2_threshold = config.R2_WARNING_THRESHOLD

        self.rmse_threshold = config.RMSE_WARNING_PERCENT

        self.mae_threshold = config.MAE_WARNING_PERCENT

        self.model_manager = ModelManager()

        self.evaluator = ModelEvaluator()

        self.feature_engineer = FeatureEngineer()

    # -------------------------------------------------------------------------

    def calculate_percentage_change(
        self,
        previous: float,
        current: float
    ) -> float:
        """
        Calculate percentage change.

        Parameters
        ----------
        previous : float

        current : float

        Returns
        -------
        float
        """

        if previous == 0:

            return 0.0

        change = (

            (current - previous)

            / abs(previous)

        ) * 100

        return round(

            float(change),

            2

        )

    # -------------------------------------------------------------------------

    def compare_metrics(
        self,
        previous_metrics: Dict,
        current_metrics: Dict
    ) -> Dict:
        """
        Compare current metrics with previous metrics.
        """

        logger.info("=" * 60)
        logger.info("Comparing Model Performance")
        logger.info("=" * 60)

        comparison = {

            "mae_change": self.calculate_percentage_change(

                previous_metrics["mae"],

                current_metrics["mae"]

            ),

            "rmse_change": self.calculate_percentage_change(

                previous_metrics["rmse"],

                current_metrics["rmse"]

            ),

            "r2_change": self.calculate_percentage_change(

                previous_metrics["r2"],

                current_metrics["r2"]

            )

        }

        logger.info(

            "Metric comparison completed."

        )

        return comparison

    # -------------------------------------------------------------------------

    def calculate_health_score(
        self,
        comparison: Dict
    ) -> int:
        """
        Calculate model health score.
        """

        logger.info("Calculating health score...")

        score = 100

        print("\n========== HEALTH DEBUG ==========")
        print("MAE Threshold :", self.mae_threshold)
        print("RMSE Threshold:", self.rmse_threshold)
        print("Comparison    :", comparison)
        print("Initial Score :", score)

        # ---------------------------------------------------------
        # MAE
        # ---------------------------------------------------------

        if comparison["mae_change"] > self.mae_threshold:
            score -= 20

        if comparison["rmse_change"] > self.rmse_threshold:
            score -= 20

        if comparison["r2_change"] < -30:
            score -= 20

        if comparison["r2_change"] < -15:
            score -= 15

        if comparison["r2_change"] < -5:
            score -= 10

        score = max(score, 0)

        logger.info(

            "Health Score : %d",

            score

        )
        print("Final Score   :", score)
        print("=================================\n")
        return score

    def calculate_current_metrics(
    self,
    dataframe: pd.DataFrame
) -> Dict:
        """
        Calculate current model metrics using
        the production model.
        """

        dataframe, _ = self.feature_engineer.prepare_features(
        dataframe
    )

        model = self.model_manager.load_model()

        y_true = dataframe[config.TARGET_COLUMN]

        X = dataframe.drop(
            columns=[config.TARGET_COLUMN]
        )

        y_pred = model.predict(X)

        training_result = {
            "y_test": y_true,
            "y_pred": y_pred
        }

        return self.evaluator.evaluate(
            training_result
        )
    # -------------------------------------------------------------------------

    def generate_report(
        self,
        previous_metrics: Dict,
        current_metrics: Dict
    ) -> Dict:
        """
        Generate complete performance monitoring report.
        """

        logger.info("=" * 60)
        logger.info("Generating Performance Report")
        logger.info("=" * 60)

        comparison = self.compare_metrics(

            previous_metrics,

            current_metrics

        )

        health_score = self.calculate_health_score(

            comparison

        )

        # ---------------------------------------------------------
        # Overall Status
        # ---------------------------------------------------------

        if health_score >= 90:

            status = "HEALTHY"
            severity = "LOW"

        elif health_score >= 70:

            status = "WARNING"
            severity = "MEDIUM"

        else:

            status = "CRITICAL"
            severity = "HIGH"

        # ---------------------------------------------------------
        # Recommendation
        # ---------------------------------------------------------

        recommendation = "Model performance is stable."

        if status == "WARNING":

            recommendation = (

                "Monitor model closely. Retraining may be required."

            )

        elif status == "CRITICAL":

            recommendation = (

                "Model retraining is strongly recommended."

            )

        performance_degraded = status != "HEALTHY"

        report = {

            "status": status,

            "severity": severity,

            "performance_degraded": performance_degraded,

            "health_score": health_score,

            "recommendation": recommendation,

            "comparison": comparison,

            "previous_metrics": previous_metrics,

            "current_metrics": current_metrics

        }

        logger.info(

            "Performance report generated successfully."

        )

        return report

    # -------------------------------------------------------------------------

    def monitor(
        self,
        dataframe: pd.DataFrame
    ) -> Dict:
        """
    Monitor production model performance.
    """

        previous_metrics = self.model_manager.load_metrics()

        print("\n========== PREVIOUS METRICS ==========")
        print(previous_metrics)

        current_metrics = self.calculate_current_metrics(
            dataframe
        )

        print("\n========== CURRENT METRICS ==========")
        print(current_metrics)

        report = self.generate_report(
            previous_metrics,
            current_metrics
        )

        print("\n========== PERFORMANCE REPORT ==========")
        print(report)

        return report
            
    
# ==============================================================================
# Standalone Testing
# ==============================================================================

if __name__ == "__main__":

    print("=" * 70)
    print("PERFORMANCE MONITOR TEST")
    print("=" * 70)

    try:

        previous_metrics = {

            "mae": 12.10,

            "rmse": 18.30,

            "r2": 0.94

        }

        current_metrics = {

            "mae": 15.40,

            "rmse": 23.60,

            "r2": 0.87

        }

        from data.generator import SalesDataGenerator

        generator = SalesDataGenerator(rows=1000)
        dataframe = generator.generate_dataset()

        monitor = PerformanceMonitor()

        report = monitor.monitor(dataframe)
        print()

        print("=" * 70)
        print("PERFORMANCE REPORT")
        print("=" * 70)

        print(

            f"Status          : {report['status']}"

        )

        print(

            f"Health Score    : {report['health_score']}"

        )

        print(

            f"Recommendation  : {report['recommendation']}"

        )

        print()

        print("Metric Comparison")

        print("-" * 50)

        print(

            f"MAE Change      : {report['comparison']['mae_change']} %"

        )

        print(

            f"RMSE Change     : {report['comparison']['rmse_change']} %"

        )

        print(

            f"R² Change       : {report['comparison']['r2_change']} %"

        )

        print()

        print("=" * 70)
        print("PERFORMANCE MONITOR TEST PASSED")
        print("=" * 70)

    except Exception as error:

        logger.exception(error)

        print()

        print("=" * 70)
        print("PERFORMANCE MONITOR TEST FAILED")
        print("=" * 70)

        print(error)