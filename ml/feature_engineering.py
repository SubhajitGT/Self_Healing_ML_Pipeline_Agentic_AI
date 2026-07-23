"""
===============================================================================
Project : Self-Healing Agentic AI ML Pipeline

File    : feature_engineering.py

Purpose :
Prepare dataset before model training.

Author  : ChatGPT
===============================================================================
"""

from __future__ import annotations

import sys
import logging
from pathlib import Path
from typing import Dict, List

# ==============================================================================
# Add Project Root
# ==============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ==============================================================================

import pandas as pd
import numpy as np

import config

# ==============================================================================
# Logging
# ==============================================================================

logger = logging.getLogger("FeatureEngineering")

logger.setLevel(config.LOG_LEVEL)

formatter = logging.Formatter(config.LOG_FORMAT)

console_handler = logging.StreamHandler(sys.stdout)

console_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(console_handler)


# ==============================================================================
# Feature Engineer
# ==============================================================================

class FeatureEngineer:
    """
    Performs feature engineering on the sales dataframe.

    Responsibilities
    ----------------
    1. Validate required columns
    2. Remove duplicate rows
    3. Handle missing values
    4. Create date features
    5. Encode categorical columns
    """

    # -------------------------------------------------------------------------

    def __init__(self):

        self.required_columns: List[str] = [

            "Transaction_ID",

            "Transaction_Date",

            "Store_ID",

            "Region",

            "Product_Category",

            "Product_ID",

            "Price",

            "Discount",

            "Marketing_Spend",

            "Competitor_Price",

            "Inventory_Level",

            "Temperature",

            "Holiday",

            "Weekend",

            "Customer_Footfall",

            config.TARGET_COLUMN

        ]

        self.metadata: Dict = {

            "rows_before": 0,

            "rows_after": 0,

            "duplicates_removed": 0,

            "missing_values_filled": 0,

            "categorical_columns_encoded": 0,

            "features_created": 0

        }

    # -------------------------------------------------------------------------

    def validate_columns(
        self,
        dataframe: pd.DataFrame
    ) -> bool:
        """
        Validate whether all required columns exist.

        Parameters
        ----------
        dataframe : pd.DataFrame

        Returns
        -------
        bool
        """

        logger.info("Validating dataset columns...")

        missing_columns = [

            column

            for column in self.required_columns

            if column not in dataframe.columns

        ]

        if missing_columns:

            logger.error(
                "Missing Columns : %s",
                missing_columns
            )

            raise ValueError(

                f"Missing required columns : {missing_columns}"

            )

        logger.info("Column validation successful.")

        return True
    # -------------------------------------------------------------------------

    def remove_duplicates(
    self,
    dataframe: pd.DataFrame
) -> pd.DataFrame:
        """
    Remove duplicate rows from the dataframe.

    Parameters
    ----------
    dataframe : pd.DataFrame

    Returns
    -------
    pd.DataFrame
        """

        logger.info("Removing duplicate rows...")

        self.metadata["rows_before"] = len(dataframe)

        duplicate_count = dataframe.duplicated().sum()

        dataframe = dataframe.drop_duplicates()

        dataframe = dataframe.reset_index(drop=True)

        self.metadata["duplicates_removed"] = int(duplicate_count)

        self.metadata["rows_after"] = len(dataframe)

        logger.info(
        "Duplicate rows removed : %d",
        duplicate_count
        )

        return dataframe
    
        # -------------------------------------------------------------------------

    def handle_missing_values(
        self,
        dataframe: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Fill missing values.

        Numeric Columns
            -> Median

        Categorical Columns
            -> Mode
        """

        logger.info("Handling missing values...")

        total_missing = int(dataframe.isna().sum().sum())

        numeric_columns = dataframe.select_dtypes(
            include=["number"]
        ).columns

        categorical_columns = dataframe.select_dtypes(
            include=["object"]
        ).columns

        # Fill numeric columns

        for column in numeric_columns:

            if dataframe[column].isna().sum() > 0:

                median = dataframe[column].median()

                dataframe[column] = dataframe[column].fillna(
                    median
                )

        # Fill categorical columns

        for column in categorical_columns:

            if dataframe[column].isna().sum() > 0:

                mode = dataframe[column].mode()

                if not mode.empty:

                    dataframe[column] = dataframe[column].fillna(
                        mode.iloc[0]
                    )

        self.metadata["missing_values_filled"] = total_missing

        logger.info(
            "Missing values filled : %d",
            total_missing
        )

        return dataframe

    # -------------------------------------------------------------------------

    def get_metadata(self) -> Dict:
        """
        Return feature engineering metadata.
        """

        return self.metadata
    
    # -------------------------------------------------------------------------

    def convert_datetime(
        self,
        dataframe: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Convert Transaction_Date column to datetime.

        Parameters
        ----------
        dataframe : pd.DataFrame

        Returns
        -------
        pd.DataFrame
        """

        logger.info("Converting Transaction_Date to datetime...")

        dataframe["Transaction_Date"] = pd.to_datetime(

            dataframe["Transaction_Date"],

            errors="coerce"

        )

        invalid_dates = dataframe["Transaction_Date"].isna().sum()

        if invalid_dates > 0:

            logger.warning(

                "%d invalid dates found. Filling using forward fill.",

                invalid_dates

            )

            dataframe["Transaction_Date"] = dataframe[
                "Transaction_Date"
            ].ffill()

        logger.info("Datetime conversion completed.")

        return dataframe


    # -------------------------------------------------------------------------

    def create_date_features(
        self,
        dataframe: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Create useful date-based features from Transaction_Date.

        Features Created
        ----------------
        Year
        Month
        Day
        DayOfWeek
        Quarter
        """

        logger.info("Creating date features...")

        dataframe["Year"] = dataframe["Transaction_Date"].dt.year

        dataframe["Month"] = dataframe["Transaction_Date"].dt.month

        dataframe["Day"] = dataframe["Transaction_Date"].dt.day

        dataframe["DayOfWeek"] = (
            dataframe["Transaction_Date"]
            .dt.dayofweek
        )

        dataframe["Quarter"] = (
            dataframe["Transaction_Date"]
            .dt.quarter
        )

        self.metadata["features_created"] += 5

        logger.info(

            "Created date features : "

            "Year, Month, Day, DayOfWeek, Quarter"

        )

        return dataframe   

    # -------------------------------------------------------------------------

    def encode_categorical_columns(
        self,
        dataframe: pd.DataFrame
    ) -> pd.DataFrame:
        """
        One-Hot Encode categorical columns.

        Parameters
        ----------
        dataframe : pd.DataFrame

        Returns
        -------
        pd.DataFrame
        """

        logger.info("Encoding categorical columns...")

        categorical_columns = [

            "Region",

            "Product_Category"

        ]

        encoded_columns = [

            column

            for column in categorical_columns

            if column in dataframe.columns

        ]

        dataframe = pd.get_dummies(

            dataframe,

            columns=encoded_columns,

            drop_first=False,

            dtype=int

        )

        self.metadata["categorical_columns_encoded"] = len(encoded_columns)

        logger.info(

            "Encoded categorical columns : %s",

            encoded_columns

        )

        return dataframe 
        
    # -------------------------------------------------------------------------

    def prepare_features(
        self,
        dataframe: pd.DataFrame
    ):
        """
        Complete feature engineering pipeline.

        Parameters
        ----------
        dataframe : pd.DataFrame

        Returns
        -------
        tuple
            (processed_dataframe, metadata)
        """

        logger.info("=" * 60)
        logger.info("Starting Feature Engineering")
        logger.info("=" * 60)

        dataframe = dataframe.copy()

        self.validate_columns(dataframe)

        dataframe = self.remove_duplicates(dataframe)

        dataframe = self.handle_missing_values(dataframe)

        dataframe = self.convert_datetime(dataframe)

        dataframe = self.create_date_features(dataframe)

        dataframe = self.encode_categorical_columns(dataframe)

        # -----------------------------------------------------
        # Remove columns not required for ML
        # -----------------------------------------------------

        columns_to_drop = [

            "Transaction_ID",

            "Transaction_Date"

        ]

        dataframe = dataframe.drop(

            columns=columns_to_drop,

            errors="ignore"

        )

        logger.info("Feature Engineering Completed")

        logger.info("=" * 60)

        return dataframe, self.get_metadata()

# ==============================================================================
# Standalone Testing
# ==============================================================================

if __name__ == "__main__":

    from data.generator import SalesDataGenerator

    generator = SalesDataGenerator(rows=100)

    df = generator.generate_dataset()

    engineer = FeatureEngineer()

    processed_df, metadata = engineer.prepare_features(df)

    print()

    print("=" * 60)

    print("Processed Dataset")

    print("=" * 60)

    print(processed_df.head())

    print()

    print("=" * 60)

    print("Columns")

    print("=" * 60)

    print(processed_df.columns.tolist())

    print()

    print("=" * 60)

    print("Metadata")

    print("=" * 60)

    for key, value in metadata.items():

        print(f"{key:<35}: {value}")

    print()

    print("=" * 60)

    print(f"Final Shape : {processed_df.shape}")

    print("=" * 60)