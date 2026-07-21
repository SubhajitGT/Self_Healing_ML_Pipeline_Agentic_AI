"""
===============================================================================
Project : Self-Healing Agentic AI ML Pipeline

File    : tools/generate_sample_data.py

Purpose :
Generate all sample datasets used in the Streamlit application.

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

import argparse
import logging
from datetime import datetime

import pandas as pd

import config
from data.generator import SalesDataGenerator
from data.drift_injector import DriftInjector

# ==============================================================================
# Logging
# ==============================================================================

logger = logging.getLogger("DatasetGenerator")
logger.setLevel(config.LOG_LEVEL)

formatter = logging.Formatter(config.LOG_FORMAT)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)

# ==============================================================================
# Helper Functions
# ==============================================================================


def create_output_directory(output_directory: Path):

    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )


# -----------------------------------------------------------------------------


def build_metadata(
    dataset_name: str,
    scenario: str,
    dataframe: pd.DataFrame
):

    metadata = pd.DataFrame(

        {

            "Property": [

                "Project",

                "Dataset Name",

                "Scenario",

                "Generated Time",

                "Rows",

                "Columns",

                "Random Seed",

                "Target Column"

            ],

            "Value": [

                config.PROJECT_NAME,

                dataset_name,

                scenario,

                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

                len(dataframe),

                len(dataframe.columns),

                config.RANDOM_SEED,

                config.TARGET_COLUMN

            ]

        }

    )

    return metadata


# -----------------------------------------------------------------------------


def save_excel(
    dataframe: pd.DataFrame,
    dataset_name: str,
    scenario: str,
    output_directory: Path
):

    file_path = output_directory / dataset_name

    metadata = build_metadata(

        dataset_name,

        scenario,

        dataframe

    )

    with pd.ExcelWriter(

        file_path,

        engine="openpyxl"

    ) as writer:

        dataframe.to_excel(

            writer,

            sheet_name=config.DATA_SHEET,

            index=False

        )

        metadata.to_excel(

            writer,

            sheet_name=config.METADATA_SHEET,

            index=False

        )

    logger.info(f"Created : {dataset_name}")


# ==============================================================================
# Generate All Datasets
# ==============================================================================


def generate_all_datasets(
    rows: int,
    output_directory: Path
):

    logger.info("Generating Base Dataset...")

    generator = SalesDataGenerator(rows)

    base_df = generator.generate_dataset()

    injector = DriftInjector()

    datasets = [

        (

            config.NORMAL_DATASET,

            "Normal Dataset",

            base_df

        ),

        (

            config.SUDDEN_DRIFT_DATASET,

            "Sudden Drift",

            injector.inject_sudden_drift(base_df)

        ),

        (

            config.GRADUAL_DRIFT_DATASET,

            "Gradual Drift",

            injector.inject_gradual_drift(base_df)

        ),

        (

            config.CONCEPT_DRIFT_DATASET,

            "Concept Drift",

            injector.inject_concept_drift(base_df)

        ),

        (

            config.MISSING_VALUE_DATASET,

            "Missing Values",

            injector.inject_missing_values(base_df)

        ),

        (

            config.OUTLIER_DATASET,

            "Outliers",

            injector.inject_outliers(base_df)

        ),

        (

            config.DUPLICATE_DATASET,

            "Duplicate Rows",

            injector.inject_duplicate_rows(base_df)

        ),

        (

            config.NEGATIVE_VALUE_DATASET,

            "Negative Values",

            injector.inject_negative_values(base_df)

        ),

        (

            config.NEW_CATEGORY_DATASET,

            "New Category",

            injector.inject_new_category(base_df)

        ),

        (

            config.BAD_SCHEMA_DATASET,

            "Bad Schema",

            injector.inject_bad_schema(base_df)

        )

    ]

    logger.info("Generating Large Dataset...")

    large_df = SalesDataGenerator(

        rows=config.LARGE_DATASET_ROWS

    ).generate_dataset()

    datasets.append(

        (

            config.LARGE_DATASET,

            "Large Dataset",

            large_df

        )

    )

    logger.info("Saving Excel Files...\n")

    for dataset_name, scenario, dataframe in datasets:

        save_excel(

            dataframe=dataframe,

            dataset_name=dataset_name,

            scenario=scenario,

            output_directory=output_directory

        )

    logger.info("All datasets generated successfully.")


# ==============================================================================
# Main
# ==============================================================================


def main():

    parser = argparse.ArgumentParser(

        description="Generate Sample Retail Sales Datasets"

    )

    parser.add_argument(

        "--rows",

        type=int,

        default=config.DEFAULT_ROWS,

        help="Rows for normal datasets"

    )

    parser.add_argument(

        "--output",

        type=str,

        default=str(config.SAMPLE_DATA_DIR),

        help="Output directory"

    )

    args = parser.parse_args()

    output_directory = Path(args.output)

    create_output_directory(output_directory)

    logger.info("=" * 70)
    logger.info(config.PROJECT_NAME)
    logger.info("=" * 70)

    logger.info(f"Output Directory : {output_directory}")
    logger.info(f"Rows             : {args.rows}")

    generate_all_datasets(

        rows=args.rows,

        output_directory=output_directory

    )

    logger.info("=" * 70)
    logger.info("Sample Dataset Generation Completed")
    logger.info("=" * 70)


# ==============================================================================
# Entry Point
# ==============================================================================

if __name__ == "__main__":

    main()