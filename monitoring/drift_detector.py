"""
===============================================================================
Project : Self-Healing Agentic AI ML Pipeline

File    : drift_detector.py

Purpose :
Detect statistical drift between reference and current datasets.

Author  : ChatGPT
===============================================================================
"""

from __future__ import annotations

import sys
import logging
from pathlib import Path
from typing import Dict, List

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

logger = logging.getLogger("DriftDetector")

logger.setLevel(config.LOG_LEVEL)

formatter = logging.Formatter(config.LOG_FORMAT)

console_handler = logging.StreamHandler(sys.stdout)

console_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(console_handler)

# ==============================================================================
# Drift Detector
# ==============================================================================


class DriftDetector:
    """
    Detect statistical drift between datasets.

    Responsibilities
    ----------------
    1. Detect numeric features
    2. Detect categorical features
    3. Calculate mean
    4. Calculate standard deviation
    5. Prepare for PSI calculation
    """

    # -------------------------------------------------------------------------

    def __init__(self):

        self.numeric_columns = config.NUMERIC_COLUMNS

        self.categorical_columns = config.CATEGORICAL_COLUMNS

        self.date_columns = config.DATE_COLUMNS

    # -------------------------------------------------------------------------

    def get_numeric_columns(
        self,
        dataframe: pd.DataFrame
    ) -> List[str]:
        """
        Return numeric columns.
        """

        logger.info("Detecting numeric columns...")

        numeric = [

            column

            for column in dataframe.columns

            if pd.api.types.is_numeric_dtype(

                dataframe[column]

            )

        ]

        logger.info(

            "Numeric Columns : %s",

            numeric

        )

        return numeric

    # -------------------------------------------------------------------------

    def get_categorical_columns(
        self,
        dataframe: pd.DataFrame
    ) -> List[str]:
        """
        Return categorical columns.
        """

        logger.info("Detecting categorical columns...")

        categorical = [

            column

            for column in dataframe.columns

            if dataframe[column].dtype == "object"

        ]

        logger.info(

            "Categorical Columns : %s",

            categorical

        )

        return categorical

    # -------------------------------------------------------------------------

    def calculate_mean(
        self,
        dataframe: pd.DataFrame
    ) -> Dict:
        """
        Calculate column means.
        """

        logger.info("Calculating means...")

        means = {}

        for column in self.get_numeric_columns(dataframe):

            means[column] = float(

                dataframe[column].mean()

            )

        return means

    # -------------------------------------------------------------------------

    def calculate_std(
        self,
        dataframe: pd.DataFrame
    ) -> Dict:
        """
        Calculate standard deviations.
        """

        logger.info("Calculating standard deviations...")

        std_values = {}

        for column in self.get_numeric_columns(dataframe):

            std_values[column] = float(

                dataframe[column].std()

            )

        return std_values

    # -------------------------------------------------------------------------

    def get_category_values(
        self,
        dataframe: pd.DataFrame
    ) -> Dict:
        """
        Return unique values of categorical columns.
        """

        logger.info("Extracting category values...")

        categories = {}

        for column in self.get_categorical_columns(dataframe):

            categories[column] = sorted(

                dataframe[column]

                .dropna()

                .astype(str)

                .unique()

                .tolist()

            )

        return categories
    
        # -------------------------------------------------------------------------

    def calculate_psi(
        self,
        expected: pd.Series,
        actual: pd.Series,
        buckets: int = None
    ) -> float:
        """
        Calculate Population Stability Index (PSI).
        """

        logger.info("Calculating PSI...")

        if buckets is None:
            buckets = config.PSI_BUCKETS

        expected = expected.dropna()
        actual = actual.dropna()

        if len(expected) == 0 or len(actual) == 0:
            return 0.0

        breakpoints = np.linspace(0, 100, buckets + 1)

        breakpoints = np.percentile(
            expected,
            breakpoints
        )

        expected_count, _ = np.histogram(
            expected,
            bins=breakpoints
        )

        actual_count, _ = np.histogram(
            actual,
            bins=breakpoints
        )

        expected_percent = expected_count / max(len(expected), 1)
        actual_percent = actual_count / max(len(actual), 1)

        expected_percent = np.where(
            expected_percent == 0,
            0.0001,
            expected_percent
        )

        actual_percent = np.where(
            actual_percent == 0,
            0.0001,
            actual_percent
        )

        psi = np.sum(
            (
                actual_percent - expected_percent
            ) *
            np.log(
                actual_percent / expected_percent
            )
        )

        return round(float(psi), 4)
    
    # -------------------------------------------------------------------------

    def detect_numeric_drift(
        self,
        reference_df: pd.DataFrame,
        current_df: pd.DataFrame
    ) -> Dict:
        """
        Detect drift in numeric columns.
        """

        logger.info("Detecting numeric drift...")

        drift = {}

        numeric_columns = self.get_numeric_columns(
            reference_df
        )

        for column in numeric_columns:

            if column not in current_df.columns:
                continue

            psi = self.calculate_psi(
                reference_df[column],
                current_df[column]
            )

            mean_shift = abs(

                current_df[column].mean()

                -

                reference_df[column].mean()

            )

            std_shift = abs(

                current_df[column].std()

                -

                reference_df[column].std()

            )

            if psi < config.PSI_LOW_THRESHOLD:

                status = "LOW"

            elif psi < config.PSI_MEDIUM_THRESHOLD:

                status = "MEDIUM"

            else:

                status = "HIGH"

            drift[column] = {

                "psi": psi,

                "mean_shift": round(
                    float(mean_shift),
                    2
                ),

                "std_shift": round(
                    float(std_shift),
                    2
                ),

                "status": status

            }

        return drift
    
    # -------------------------------------------------------------------------

    def detect_category_drift(
        self,
        reference_df: pd.DataFrame,
        current_df: pd.DataFrame
    ) -> Dict:
        """
        Detect new categorical values.
        """

        logger.info("Detecting category drift...")

        category_drift = {}

        categorical_columns = self.get_categorical_columns(
            reference_df
        )

        for column in categorical_columns:

            if column not in current_df.columns:
                continue

            reference_values = set(

                reference_df[column]

                .dropna()

                .astype(str)

            )

            current_values = set(

                current_df[column]

                .dropna()

                .astype(str)

            )

            new_values = sorted(

                list(

                    current_values -

                    reference_values

                )

            )

            category_drift[column] = {

                "new_categories": new_values,

                "count": len(new_values)

            }

        return category_drift
    
    # -------------------------------------------------------------------------

    def generate_drift_report(
        self,
        reference_df: pd.DataFrame,
        current_df: pd.DataFrame
    ) -> Dict:
        """
        Generate complete drift report.
        """

        logger.info("=" * 60)
        logger.info("Generating Drift Report")
        logger.info("=" * 60)

        numeric_drift = self.detect_numeric_drift(

            reference_df,

            current_df

        )

        category_drift = self.detect_category_drift(

            reference_df,

            current_df

        )

        drift_score = 0

        for value in numeric_drift.values():

            if value["status"] == "HIGH":

                drift_score += 20

            elif value["status"] == "MEDIUM":

                drift_score += 10

        drift_score = min(

            drift_score,

            100

        )

        if drift_score < 20:

            overall = "LOW"

        elif drift_score < 50:

            overall = "MODERATE"

        else:

            overall = "HIGH"

        return {

            "status": overall,

            "drift_score": drift_score,

            "numeric_drift": numeric_drift,

            "category_drift": category_drift

        }
    
    # -------------------------------------------------------------------------

    def detect(
        self,
        reference_df: pd.DataFrame,
        current_df: pd.DataFrame
    ) -> Dict:
        """
        Public API.
        """

        return self.generate_drift_report(

            reference_df,

            current_df

        )
    
# ==============================================================================
# Standalone Testing
# ==============================================================================

if __name__ == "__main__":

    from data.generator import SalesDataGenerator
    from data.drift_injector import DriftInjector

    print("=" * 70)
    print("DRIFT DETECTOR TEST")
    print("=" * 70)

    try:

        generator = SalesDataGenerator(rows=1000)

        reference_df = generator.generate_dataset()

        injector = DriftInjector()

        current_df = injector.inject_sudden_drift(

            reference_df.copy()

        )

        detector = DriftDetector()

        report = detector.detect(

            reference_df,

            current_df

        )

        print()

        print("=" * 70)
        print("DRIFT REPORT")
        print("=" * 70)

        print("Overall Status :", report["status"])
        print("Drift Score    :", report["drift_score"])

        print()

        print("Numeric Drift")

        print("-" * 60)

        for feature, value in report["numeric_drift"].items():

            print(

                f"{feature:20} "

                f"PSI={value['psi']:.4f} "

                f"Status={value['status']}"

            )

        print()

        print("Category Drift")

        print("-" * 60)

        for feature, value in report["category_drift"].items():

            if value["count"] > 0:

                print(

                    feature,

                    ":",

                    value["new_categories"]

                )

        print()

        print("=" * 70)
        print("DRIFT DETECTOR TEST PASSED")
        print("=" * 70)

    except Exception as error:

        logger.exception(error)

        print()

        print("=" * 70)
        print("DRIFT DETECTOR TEST FAILED")
        print("=" * 70)

        print(error)