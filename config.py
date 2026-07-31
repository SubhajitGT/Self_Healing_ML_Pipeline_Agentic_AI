"""
===============================================================================
Project : Self-Healing Agentic AI ML Pipeline

File    : config.py

Purpose :
Master configuration for the complete project.

Author  : ChatGPT
===============================================================================
"""

from pathlib import Path
import logging

import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass



# ==============================================================================
# Project Information
# ==============================================================================

PROJECT_NAME = "Self-Healing Agentic AI ML Pipeline"

VERSION = "1.0.0"

# ==============================================================================
# Project Paths
# ==============================================================================

PROJECT_ROOT = Path(__file__).resolve().parent

DATA_DIR = PROJECT_ROOT / "data"

TOOLS_DIR = PROJECT_ROOT / "tools"

DATABASE_DIR = PROJECT_ROOT / "database"

MODEL_DIR = PROJECT_ROOT / "models"

SAVED_MODEL_DIR = MODEL_DIR / "saved_models"

LOG_DIR = PROJECT_ROOT / "logs"

OUTPUT_DIR = PROJECT_ROOT / "output"

SAMPLE_DATA_DIR = OUTPUT_DIR / "sample_datasets"

MONITORING_DIR = PROJECT_ROOT / "monitoring"

# Automatically create folders

for directory in [

    DATA_DIR,

    TOOLS_DIR,

    DATABASE_DIR,

    MODEL_DIR,

    SAVED_MODEL_DIR,

    LOG_DIR,

    OUTPUT_DIR,

    SAMPLE_DATA_DIR,

    MONITORING_DIR

]:

    directory.mkdir(
        parents=True,
        exist_ok=True
    )

# ==============================================================================
# Logging
# ==============================================================================

LOG_LEVEL = logging.INFO

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

# ==============================================================================
# SQLite Database
# ==============================================================================

DATABASE_NAME = "self_healing_pipeline.db"

SQLITE_DB_NAME = DATABASE_NAME

SQLITE_DB_PATH = DATABASE_DIR / DATABASE_NAME

# ==============================================================================
# Random Seed
# ==============================================================================

RANDOM_SEED = 42

DEFAULT_RANDOM_SEED = RANDOM_SEED

# ==============================================================================
# Dataset Configuration
# ==============================================================================

# ==============================================================================
# Dataset Configuration
# ==============================================================================

TARGET_COLUMN = "Sales"

DATE_COLUMN = "Transaction_Date"

REQUIRED_COLUMNS = [

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

    TARGET_COLUMN

]

NUMERIC_COLUMNS = [

    "Price",

    "Discount",

    "Marketing_Spend",

    "Competitor_Price",

    "Inventory_Level",

    "Temperature",

    "Customer_Footfall",

    TARGET_COLUMN

]

DATE_COLUMNS = [

    DATE_COLUMN

]

NON_NEGATIVE_COLUMNS = [

    "Price",

    "Marketing_Spend",

    "Inventory_Level",

    "Customer_Footfall",

    TARGET_COLUMN

]

CATEGORICAL_COLUMNS = [

    "Region",

    "Product_Category"

]
# ==============================================================================
# Validation Configuration
# ==============================================================================

MAX_ALLOWED_MISSING_PERCENT = 20

MAX_ALLOWED_DUPLICATES = 0

MIN_HEALTH_SCORE = 70

# ==============================================================================
# Supported File Types
# ==============================================================================

SUPPORTED_FILE_TYPES = [

    ".xlsx",

    ".xls",

    ".csv"

]

# ==============================================================================
# Date Formats
# ==============================================================================

DATE_FORMAT = "%Y-%m-%d"

TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

# ==============================================================================
# Sample Dataset Generation
# ==============================================================================

# Default number of rows

DEFAULT_ROWS = 1000

DEFAULT_SAMPLE_ROWS = DEFAULT_ROWS

# Dataset start date

DATE_START = "2023-01-01"

# ------------------------------------------------------------------------------
# Regions
# ------------------------------------------------------------------------------

REGIONS = [

    "North",

    "South",

    "East",

    "West"

]

# ------------------------------------------------------------------------------
# Product Categories
# ------------------------------------------------------------------------------

PRODUCT_CATEGORIES = [

    "Electronics",

    "Furniture",

    "Clothing",

    "Sports",

    "Groceries"

]

# ------------------------------------------------------------------------------
# Dataset Size
# ------------------------------------------------------------------------------

NUMBER_OF_PRODUCTS = 50

NUMBER_OF_STORES = 25

LARGE_DATASET_ROWS = 100000

# ------------------------------------------------------------------------------
# Base Values
# ------------------------------------------------------------------------------

BASE_SALES = 500

BASE_PRICE = 1200

BASE_MARKETING = 5000

BASE_TEMPERATURE = 28

BASE_INVENTORY = 400

BASE_COMPETITOR_PRICE = 1180

BASE_FOOTFALL = 350

# ------------------------------------------------------------------------------
# Standard Deviations
# ------------------------------------------------------------------------------

PRICE_STD = 150

MARKETING_STD = 800

TEMPERATURE_STD = 6

INVENTORY_STD = 60

COMPETITOR_STD = 120

FOOTFALL_STD = 70

RANDOM_NOISE_STD = 50

# ------------------------------------------------------------------------------
# Feature Weights
# ------------------------------------------------------------------------------

PRICE_WEIGHT = -0.18

MARKETING_WEIGHT = 0.06

TEMPERATURE_WEIGHT = 2.5

INVENTORY_WEIGHT = 0.15

COMPETITOR_WEIGHT = -0.12

FOOTFALL_WEIGHT = 0.42

# ------------------------------------------------------------------------------
# Holiday & Weekend Effects
# ------------------------------------------------------------------------------

HOLIDAY_BONUS = 250

WEEKEND_BONUS = 120

# ------------------------------------------------------------------------------
# Discount Range
# ------------------------------------------------------------------------------

DISCOUNT_MIN = 0

DISCOUNT_MAX = 40

# ==============================================================================
# Drift Injection
# ==============================================================================

SUDDEN_DRIFT_PERCENT = 40

GRADUAL_DRIFT_PERCENT = 20

CONCEPT_DRIFT_PERCENT = 30

MISSING_VALUE_PERCENT = 10

OUTLIER_PERCENT = 2

DUPLICATE_PERCENT = 5

NEGATIVE_VALUE_PERCENT = 2

NEW_CATEGORY_PERCENT = 8

# ==============================================================================
# Output Excel Files
# ==============================================================================

NORMAL_DATASET = "sales_normal.xlsx"

SUDDEN_DRIFT_DATASET = "sales_sudden_drift.xlsx"

GRADUAL_DRIFT_DATASET = "sales_gradual_drift.xlsx"

CONCEPT_DRIFT_DATASET = "sales_concept_drift.xlsx"

MISSING_VALUE_DATASET = "sales_missing_values.xlsx"

OUTLIER_DATASET = "sales_outliers.xlsx"

DUPLICATE_DATASET = "sales_duplicate_rows.xlsx"

NEGATIVE_VALUE_DATASET = "sales_negative_values.xlsx"

NEW_CATEGORY_DATASET = "sales_new_category.xlsx"

BAD_SCHEMA_DATASET = "sales_bad_schema.xlsx"

LARGE_DATASET = "sales_large_dataset.xlsx"

# ==============================================================================
# Excel Sheet Names
# ==============================================================================

DATA_SHEET = "Sales_Data"

METADATA_SHEET = "Metadata"

# ==============================================================================
# Feature Engineering
# ==============================================================================

# Remove duplicate rows before training
DROP_DUPLICATES = True

# Fill missing numeric values
FILL_NUMERIC_NA = 0

# Fill missing categorical values
FILL_CATEGORICAL_NA = "Unknown"

# Enable categorical encoding
ENABLE_LABEL_ENCODING = True

# ==============================================================================
# Machine Learning
# ==============================================================================

# Train-Test Split
TEST_SIZE = 0.20

# Model Hyperparameters
N_ESTIMATORS = 100

LEARNING_RATE = 0.10

MAX_DEPTH = 5

# ==============================================================================
# Model Storage
# ==============================================================================

MODEL_NAME = "sales_forecaster"

MODEL_EXTENSION = ".pkl"

DEFAULT_MODEL_VERSION = 1

MODEL_FILE_NAME = f"{MODEL_NAME}_v{DEFAULT_MODEL_VERSION}{MODEL_EXTENSION}"
MODEL_METADATA_NAME = f"{MODEL_NAME}_metadata.json"

# ==============================================================================
# Model Evaluation
# ==============================================================================

EVALUATION_METRICS = [

    "mae",

    "rmse",

    "r2"

]

# ==============================================================================
# Drift Detection
# ==============================================================================

# PSI Configuration

PSI_BUCKETS = 10

# PSI Interpretation
#
# < 0.10  -> No Drift
# 0.10-0.25 -> Moderate Drift
# >0.25 -> Significant Drift

PSI_LOW_THRESHOLD = 0.10

PSI_MEDIUM_THRESHOLD = 0.25

PSI_HIGH_THRESHOLD = 0.50

# Statistical Drift

MEAN_SHIFT_THRESHOLD = 0.15

STD_SHIFT_THRESHOLD = 0.15

HIGH_DRIFT_SCORE = 20

MEDIUM_DRIFT_SCORE = 10

CATEGORY_DRIFT_SCORE = 5

# ==============================================================================
# Performance Monitoring
# ==============================================================================

R2_WARNING_THRESHOLD = 0.85

RMSE_WARNING_PERCENT = 20

MAE_WARNING_PERCENT = 20

VALIDATION_ERROR_PENALTY = 20

VALIDATION_WARNING_PENALTY = 5

MINIMUM_DATASET_ROWS = 100

# ==============================================================================
# Gemini Configuration
# ==============================================================================

# Fill these before running Gemini modules

try:
    import streamlit as st
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    GEMINI_MODEL = st.secrets["GEMINI_MODEL"]
except Exception:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)

GEMINI_TEMPERATURE = 0.2

MAX_OUTPUT_TOKENS = 2048

# ==============================================================================
# Streamlit Configuration
# ==============================================================================

APP_TITLE = "Self-Healing Agentic AI ML Pipeline"

PAGE_ICON = "🤖"

LAYOUT = "wide"

SIDEBAR_STATE = "expanded"

# ==============================================================================
# Report Configuration
# ==============================================================================

SAVE_REPORTS = True

REPORT_DIRECTORY = OUTPUT_DIR / "reports"

REPORT_DIRECTORY.mkdir(

    parents=True,

    exist_ok=True

)

# ==============================================================================
# Versioning
# ==============================================================================

MODEL_REGISTRY_TABLE = "model_registry"

TRAINING_HISTORY_TABLE = "training_history"

PREDICTION_HISTORY_TABLE = "prediction_history"

DRIFT_HISTORY_TABLE = "drift_history"

VALIDATION_HISTORY_TABLE = "validation_history"

# ==============================================================================
# Backward Compatibility
# ==============================================================================

# Random


# Dataset



# SQLite

SQLITE_DATABASE = SQLITE_DB_PATH

# Model

MODEL_PATH = SAVED_MODEL_DIR

# Output

REPORTS_DIR = REPORT_DIRECTORY


SUPPORTED_MODELS = [

    "GradientBoostingRegressor"

]

"""
===============================================================================
Dashboard Configuration
===============================================================================
"""

# ==============================================================================
# Application
# ==============================================================================

APP_NAME = "Self-Healing Agentic AI ML Pipeline"

APP_VERSION = "1.0"

PAGE_LAYOUT = "wide"

PAGE_ICON = "🤖"

# ==============================================================================
# Upload Configuration
# ==============================================================================

SUPPORTED_FILE_TYPES = [

    "csv",

    "xlsx"

]

MAX_UPLOAD_SIZE_MB = 200

# ==============================================================================
# Workflow Stages
# ==============================================================================

WORKFLOW_STAGES = (

    "HOME",

    "UPLOAD",

    "VALIDATION",

    "EXPLORER",

    "MONITORING",

    "AI_DIAGNOSIS",

    "SELF_HEALING",

    "MODEL_EVOLUTION",

    "PREDICTION",

    "HISTORY"

)

# ==============================================================================
# Workflow Progress
# ==============================================================================

WORKFLOW_PROGRESS = {

    "HOME": 0,

    "UPLOAD": 10,

    "VALIDATION": 20,

    "EXPLORER": 35,

    "MONITORING": 50,

    "AI_DIAGNOSIS": 65,

    "SELF_HEALING": 80,

    "MODEL_EVOLUTION": 90,

    "PREDICTION": 95,

    "HISTORY": 100

}

# ==============================================================================
# Model
# ==============================================================================

DEFAULT_MODEL_VERSION = 1

MODEL_VERSION_PREFIX = "Version"

# ==============================================================================
# Session Keys
# ==============================================================================

SESSION_KEYS = (

    "uploaded_df",

    "validated_df",

    "prediction_df",

    "reference_df",

    "validation_report",

    "monitoring_report",

    "ai_report",

    "self_healing_result",

    "prediction_result",

    "execution_history",

    "training_profile",

    "retrained_profile",

    "current_model_version",

    "candidate_model_version",

    "workflow_stage",

    "workflow_completed",

    "processing",

    "last_error",

    "uploaded_filename"

)

# ==============================================================================
# Status Labels
# ==============================================================================

STATUS_HEALTHY = "Healthy"

STATUS_READY = "Ready"

STATUS_ENABLED = "Enabled"

STATUS_COMPLETED = "Completed"

STATUS_IN_PROGRESS = "In Progress"

STATUS_FAILED = "Failed"

# ==============================================================================
# Dashboard Messages
# ==============================================================================

MSG_UPLOAD_FIRST = "Please upload a dataset first."

MSG_VALIDATE_FIRST = "Please validate the uploaded dataset first."

MSG_MONITORING_FIRST = "Please complete Monitoring before AI Diagnosis."

MSG_AI_FIRST = "Please complete AI Diagnosis before Self-Healing."

MSG_SELF_HEALING_FIRST = "Please complete Self-Healing before Model Evolution."

MSG_PREDICTION_FIRST = "Please complete Validation before Prediction."

MSG_HISTORY_EMPTY = "No execution history available."

# ==============================================================================
# Footer
# ==============================================================================

FOOTER_TEXT = (
    "Self-Healing Agentic AI ML Pipeline | Version 1.0"
)