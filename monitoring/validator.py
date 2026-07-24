"""
===============================================================================
Project : Self-Healing Agentic AI ML Pipeline

File    : validator.py

Purpose :
Validate uploaded datasets before ML pipeline execution.

Author  : ChatGPT
===============================================================================
"""

from __future__ import annotations

import sys
import logging
from pathlib import Path
from typing import Dict, List

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

logger = logging.getLogger("DatasetValidator")

logger.setLevel(config.LOG_LEVEL)

formatter = logging.Formatter(config.LOG_FORMAT)

console_handler = logging.StreamHandler(sys.stdout)

console_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(console_handler)

# ==============================================================================
# Dataset Validator
# ==============================================================================


class DatasetValidator:
    """
    Validate uploaded dataset before feature engineering.

    Responsibilities
    ----------------
    1. Empty dataset validation
    2. Required column validation
    3. Missing value validation
    4. Duplicate row validation
    """

    # -------------------------------------------------------------------------

    def __init__(self):

        self.required_columns = config.REQUIRED_COLUMNS

        self.target_column = config.TARGET_COLUMN

    # -------------------------------------------------------------------------

    def validate_empty_dataset(
        self,
        dataframe: pd.DataFrame
    ) -> List[str]:
        """
        Validate dataframe is not empty.
        """

        logger.info("Checking empty dataset...")

        errors = []

        if dataframe is None:

            errors.append("Dataset is None.")

            return errors

        if dataframe.empty:

            errors.append("Dataset is empty.")

        return errors

    # -------------------------------------------------------------------------

    def validate_required_columns(
        self,
        dataframe: pd.DataFrame
    ) -> List[str]:
        """
        Validate required columns exist.
        """

        logger.info("Checking required columns...")

        errors = []

        for column in self.required_columns:

            if column not in dataframe.columns:

                errors.append(
                    f"Missing required column : {column}"
                )

        return errors

    # -------------------------------------------------------------------------

    def validate_missing_values(
        self,
        dataframe: pd.DataFrame
    ) -> Dict:
        """
        Check missing values.
        """

        logger.info("Checking missing values...")

        warnings = []

        missing_summary = {}

        missing = dataframe.isnull().sum()

        for column, count in missing.items():

            if count > 0:

                warnings.append(

                    f"{column} contains {count} missing values."

                )

                missing_summary[column] = int(count)

        return {

            "warnings": warnings,

            "summary": missing_summary

        }

    # -------------------------------------------------------------------------

    def validate_duplicate_rows(
        self,
        dataframe: pd.DataFrame
    ) -> Dict:
        """
        Check duplicate rows.
        """

        logger.info("Checking duplicate rows...")

        duplicate_count = int(

            dataframe.duplicated().sum()

        )

        warnings = []

        if duplicate_count > 0:

            warnings.append(

                f"{duplicate_count} duplicate rows found."

            )

        return {

            "warnings": warnings,

            "duplicate_count": duplicate_count

        }
    # -------------------------------------------------------------------------

    def validate_numeric_columns(
        self,
        dataframe: pd.DataFrame
    ) -> List[str]:
        """
        Validate numeric columns.
        """

        logger.info("Checking numeric columns...")

        errors = []

        numeric_columns = [

            self.target_column

        ]

        for column in numeric_columns:

            if column not in dataframe.columns:

                continue

            if not pd.api.types.is_numeric_dtype(

                dataframe[column]

            ):

                errors.append(

                    f"{column} should be numeric."

                )

        return errors
    
    # -------------------------------------------------------------------------

    def validate_negative_values(
        self,
        dataframe: pd.DataFrame
    ) -> List[str]:
        """
        Check negative values.
        """

        logger.info("Checking negative values...")

        warnings = []

        if self.target_column in dataframe.columns:

            negative_count = int(

                (dataframe[self.target_column] < 0).sum()

            )

            if negative_count > 0:

                warnings.append(

                    f"{negative_count} negative values found in {self.target_column}."

                )

        return warnings
    
    # -------------------------------------------------------------------------

    def validate_schema(
        self,
        dataframe: pd.DataFrame
    ) -> Dict:
        """
        Validate dataframe schema.
        """

        logger.info("Validating schema...")

        expected = set(

            self.required_columns

        )

        actual = set(

            dataframe.columns

        )

        missing = sorted(

            expected - actual

        )

        additional = sorted(

            actual - expected

        )

        return {

            "missing_columns": missing,

            "additional_columns": additional,

            "schema_valid": len(missing) == 0

        }
    
    # -------------------------------------------------------------------------

    def generate_validation_report(

        self,

        dataframe: pd.DataFrame

    ) -> Dict:
        """
        Generate complete validation report.
        """

        logger.info("=" * 60)

        logger.info("Generating Validation Report")

        logger.info("=" * 60)

        errors = []

        warnings = []

        health_score = 100

        # ---------------------------------------------------------

        errors.extend(

            self.validate_empty_dataset(dataframe)

        )

        errors.extend(

            self.validate_required_columns(dataframe)

        )

        errors.extend(

            self.validate_numeric_columns(dataframe)

        )

        # ---------------------------------------------------------

        missing_result = self.validate_missing_values(

            dataframe

        )

        warnings.extend(

            missing_result["warnings"]

        )

        duplicate_result = self.validate_duplicate_rows(

            dataframe

        )

        warnings.extend(

            duplicate_result["warnings"]

        )

        warnings.extend(

            self.validate_negative_values(

                dataframe

            )

        )

        schema_result = self.validate_schema(

            dataframe

        )

        # ---------------------------------------------------------
        # Health Score
        # ---------------------------------------------------------

        health_score -= len(errors) * 20

        health_score -= len(warnings) * 5

        health_score = max(

            health_score,

            0

        )

        status = "PASS"

        if len(errors) > 0:

            status = "FAIL"

        report = {

            "status": status,

            "health_score": health_score,

            "errors": errors,

            "warnings": warnings,

            "summary": {

                "rows": len(dataframe),

                "columns": len(dataframe.columns),

                "duplicate_rows": duplicate_result["duplicate_count"],

                "missing_values": missing_result["summary"],

                "schema": schema_result

            }

        }

        logger.info(

            "Validation completed."

        )

        return report
    
    # -------------------------------------------------------------------------

    def validate(

        self,

        dataframe: pd.DataFrame

    ) -> Dict:
        """
        Public validation method.
        """

        return self.generate_validation_report(

            dataframe

        )
    
# ==============================================================================
# Standalone Testing
# ==============================================================================

if __name__ == "__main__":

    from data.generator import SalesDataGenerator

    print("=" * 70)

    print("DATASET VALIDATOR TEST")

    print("=" * 70)

    try:

        generator = SalesDataGenerator(

            rows=1000

        )

        dataframe = generator.generate_dataset()

        validator = DatasetValidator()

        report = validator.validate(

            dataframe

        )

        print()

        print("=" * 70)

        print("VALIDATION REPORT")

        print("=" * 70)

        print(

            f"Status         : {report['status']}"

        )

        print(

            f"Health Score   : {report['health_score']}"

        )

        print(

            f"Rows           : {report['summary']['rows']}"

        )

        print(

            f"Columns        : {report['summary']['columns']}"

        )

        print(

            f"Duplicate Rows : {report['summary']['duplicate_rows']}"

        )

        print()

        print("Errors")

        print("-" * 40)

        if report["errors"]:

            for error in report["errors"]:

                print(error)

        else:

            print("None")

        print()

        print("Warnings")

        print("-" * 40)

        if report["warnings"]:

            for warning in report["warnings"]:

                print(warning)

        else:

            print("None")

        print()

        print("=" * 70)

        print("VALIDATOR TEST PASSED")

        print("=" * 70)

    except Exception as error:

        logger.exception(error)

        print()

        print("=" * 70)

        print("VALIDATOR TEST FAILED")

        print("=" * 70)

        print(error)