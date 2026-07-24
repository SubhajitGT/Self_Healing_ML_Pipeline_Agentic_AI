"""
===============================================================================
Project : Self-Healing Agentic AI ML Pipeline

File    : config.py

Purpose :
Central configuration file for the complete project.

Author  : ChatGPT
===============================================================================
"""

from pathlib import Path
import logging

# ==============================================================================
# Project Paths
# ==============================================================================

PROJECT_ROOT = Path(__file__).resolve().parent

DATA_DIR = PROJECT_ROOT / "data"

DATABASE_DIR = PROJECT_ROOT / "database"

MODEL_DIR = PROJECT_ROOT / "models"

SAVED_MODEL_DIR = MODEL_DIR / "saved_models"

LOG_DIR = PROJECT_ROOT / "logs"

OUTPUT_DIR = PROJECT_ROOT / "output"

# Create directories automatically

for directory in [

    DATA_DIR,

    DATABASE_DIR,

    MODEL_DIR,

    SAVED_MODEL_DIR,

    LOG_DIR,

    OUTPUT_DIR

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

SQLITE_DB_NAME = "self_healing_pipeline.db"

SQLITE_DB_PATH = DATABASE_DIR / SQLITE_DB_NAME

# ==============================================================================
# Dataset Configuration
# ==============================================================================

TARGET_COLUMN = "Sales"

DATE_COLUMN = "Date"

# Required columns in uploaded Excel

REQUIRED_COLUMNS = [

    "Date",

    "Region",

    "Product",

    "Category",

    TARGET_COLUMN

]

# Numeric columns

NUMERIC_COLUMNS = [

    TARGET_COLUMN

]

# Date columns

DATE_COLUMNS = [

    DATE_COLUMN

]

# Columns where negative values are not allowed

NON_NEGATIVE_COLUMNS = [

    TARGET_COLUMN

]

# Categorical columns

CATEGORICAL_COLUMNS = [

    "Region",

    "Product",

    "Category"

]

# ==============================================================================
# Sample Dataset Generation
# ==============================================================================

DEFAULT_SAMPLE_ROWS = 1000

DEFAULT_RANDOM_SEED = 42

# ==============================================================================
# Feature Engineering
# ==============================================================================

DROP_DUPLICATES = True

FILL_NUMERIC_NA = 0

FILL_CATEGORICAL_NA = "Unknown"

ENABLE_LABEL_ENCODING = True

# ==============================================================================
# Machine Learning
# ==============================================================================

TEST_SIZE = 0.20

RANDOM_SEED = 42

N_ESTIMATORS = 100

LEARNING_RATE = 0.10

MAX_DEPTH = 5

# ==============================================================================
# Model Storage
# ==============================================================================

MODEL_NAME = "sales_forecaster"

MODEL_EXTENSION = ".pkl"

DEFAULT_MODEL_VERSION = 1

# ==============================================================================
# Drift Detection
# ==============================================================================

PSI_BUCKETS = 10

PSI_LOW_THRESHOLD = 0.10

PSI_MEDIUM_THRESHOLD = 0.25

PSI_HIGH_THRESHOLD = 0.50

MEAN_SHIFT_THRESHOLD = 0.15

STD_SHIFT_THRESHOLD = 0.15

# ==============================================================================
# Performance Monitoring
# ==============================================================================

R2_WARNING_THRESHOLD = 0.85

RMSE_WARNING_PERCENT = 20

MAE_WARNING_PERCENT = 20

# ==============================================================================
# Dataset Validation
# ==============================================================================

MAX_ALLOWED_MISSING_PERCENT = 20

MAX_ALLOWED_DUPLICATES = 0

MIN_HEALTH_SCORE = 70

# ==============================================================================
# Gemini Configuration
# ==============================================================================

GEMINI_MODEL = ""

GEMINI_API_KEY = ""

GEMINI_TEMPERATURE = 0.2

MAX_OUTPUT_TOKENS = 2048

# ==============================================================================
# Streamlit
# ==============================================================================

APP_TITLE = "Self-Healing Agentic AI ML Pipeline"

PAGE_ICON = "🤖"

LAYOUT = "wide"

# ==============================================================================
# Miscellaneous
# ==============================================================================

DATE_FORMAT = "%Y-%m-%d"

TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

SUPPORTED_FILE_TYPES = [

    ".xlsx",

    ".xls",

    ".csv"

]