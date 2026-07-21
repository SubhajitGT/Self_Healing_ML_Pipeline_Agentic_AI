"""
===============================================================================
Project : Self-Healing Agentic AI ML Pipeline

File    : data/drift_injector.py

Purpose :
Inject different kinds of drift and data quality issues into a clean dataset.

Author  : ChatGPT
===============================================================================
"""

from __future__ import annotations

import sys
from pathlib import Path

# ==============================================================================
# Add Project Root to Python Path
# ==============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ==============================================================================

import numpy as np
import pandas as pd

import config


class DriftInjector:
    """
    Injects various types of drift and data quality issues into
    an existing dataframe.

    Each method returns a NEW dataframe.
    """

    def __init__(
        self,
        random_seed: int = config.RANDOM_SEED
    ):

        self.random_seed = random_seed
        np.random.seed(self.random_seed)

    # -------------------------------------------------------------------------

    @staticmethod
    def _copy(df: pd.DataFrame) -> pd.DataFrame:
        """Return deep copy of dataframe."""
        return df.copy(deep=True)

    # -------------------------------------------------------------------------

    def inject_sudden_drift(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Simulates sudden business change.

        Marketing Spend ↑
        Customer Footfall ↑
        Competitor Price ↓
        """

        drift_df = self._copy(df)

        split_index = int(len(drift_df) * 0.70)

        affected_rows = drift_df.index >= split_index

        marketing_factor = np.random.uniform(2.0, 3.0)
        footfall_factor = np.random.uniform(1.4, 1.8)
        competitor_factor = np.random.uniform(0.8, 0.95)

        drift_df.loc[
            affected_rows,
            "Marketing_Spend"
        ] *= marketing_factor

        drift_df.loc[
            affected_rows,
            "Customer_Footfall"
        ] *= footfall_factor

        drift_df.loc[
            affected_rows,
            "Competitor_Price"
        ] *= competitor_factor

        return drift_df

    # -------------------------------------------------------------------------

    def inject_gradual_drift(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Marketing Spend slowly increases over time.
        """

        drift_df = self._copy(df)

        multiplier = np.linspace(
            1.0,
            2.0,
            len(drift_df)
        )

        drift_df["Marketing_Spend"] *= multiplier

        drift_df["Customer_Footfall"] *= np.linspace(
            1.0,
            1.5,
            len(drift_df)
        )

        return drift_df

    # -------------------------------------------------------------------------

    def inject_concept_drift(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Feature distribution remains similar,
        but target relationship changes.

        Marketing increases
        while Sales decrease.
        """

        drift_df = self._copy(df)

        split_index = int(len(drift_df) * 0.60)

        affected_rows = drift_df.index >= split_index

        drift_df.loc[
            affected_rows,
            "Marketing_Spend"
        ] *= np.random.uniform(1.5, 2.5)

        drift_df.loc[
            affected_rows,
            "Sales"
        ] *= np.random.uniform(0.45, 0.70)

        drift_df["Sales"] = drift_df["Sales"].round(2)

        return drift_df

    # -------------------------------------------------------------------------

    def inject_missing_values(
        self,
        df: pd.DataFrame,
        percentage: float = 0.05
    ) -> pd.DataFrame:
        """
        Randomly inserts missing values.
        """

        drift_df = self._copy(df)

        columns = [

            "Price",

            "Marketing_Spend",

            "Inventory_Level",

            "Competitor_Price"

        ]

        rows = int(len(drift_df) * percentage)

        for column in columns:

            random_index = np.random.choice(

                drift_df.index,

                rows,

                replace=False

            )

            drift_df.loc[random_index, column] = np.nan

        return drift_df

    # -------------------------------------------------------------------------

    def inject_outliers(
        self,
        df: pd.DataFrame,
        percentage: float = 0.02
    ) -> pd.DataFrame:
        """
        Inject extreme numerical values.
        """

        drift_df = self._copy(df)

        rows = int(len(drift_df) * percentage)

        random_index = np.random.choice(

            drift_df.index,

            rows,

            replace=False

        )

        drift_df.loc[
            random_index,
            "Marketing_Spend"
        ] *= 8

        drift_df.loc[
            random_index,
            "Price"
        ] *= 5

        drift_df.loc[
            random_index,
            "Inventory_Level"
        ] *= 4

        return drift_df

    # -------------------------------------------------------------------------

    def inject_duplicate_rows(
        self,
        df: pd.DataFrame,
        percentage: float = 0.05
    ) -> pd.DataFrame:
        """
        Duplicate random rows.
        """

        drift_df = self._copy(df)

        duplicates = drift_df.sample(

            frac=percentage,

            random_state=self.random_seed

        )

        drift_df = pd.concat(

            [

                drift_df,

                duplicates

            ],

            ignore_index=True

        )

        return drift_df

    # -------------------------------------------------------------------------

    def inject_negative_values(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Creates invalid business values.
        """

        drift_df = self._copy(df)

        random_index = np.random.choice(

            drift_df.index,

            20,

            replace=False

        )

        drift_df.loc[
            random_index,
            "Price"
        ] *= -1

        drift_df.loc[
            random_index,
            "Inventory_Level"
        ] *= -1

        drift_df.loc[
            random_index,
            "Marketing_Spend"
        ] *= -1

        return drift_df

    # -------------------------------------------------------------------------

    def inject_new_category(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Introduce unseen category.
        """

        drift_df = self._copy(df)

        random_index = np.random.choice(

            drift_df.index,

            100,

            replace=False

        )

        drift_df.loc[
            random_index,
            "Product_Category"
        ] = "Luxury"

        return drift_df

    # -------------------------------------------------------------------------

    def inject_bad_schema(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Simulate schema mismatch.
        """

        drift_df = self._copy(df)

        drift_df.rename(

            columns={

                "Marketing_Spend": "Marketing"

            },

            inplace=True

        )

        drift_df["Price"] = drift_df["Price"].astype(str)

        drift_df.loc[
            drift_df.index[:20],
            "Price"
        ] = "INVALID"

        return drift_df


# ==============================================================================
# Standalone Testing
# ==============================================================================

if __name__ == "__main__":

    from data.generator import SalesDataGenerator

    generator = SalesDataGenerator(rows=1000)

    clean_df = generator.generate_dataset()

    injector = DriftInjector()

    sudden = injector.inject_sudden_drift(clean_df)

    gradual = injector.inject_gradual_drift(clean_df)

    concept = injector.inject_concept_drift(clean_df)

    print("Original Shape :", clean_df.shape)

    print("Sudden Drift :", sudden.shape)

    print("Gradual Drift :", gradual.shape)

    print("Concept Drift :", concept.shape)