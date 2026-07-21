"""
===============================================================================
Project : Self-Healing Agentic AI ML Pipeline
File    : config.py
Purpose : Central Configuration File
===============================================================================
"""

from pathlib import Path

# ==============================================================================
# PROJECT INFORMATION
# ==============================================================================

PROJECT_NAME = "Self-Healing Agentic AI ML Pipeline"

VERSION = "1.0.0"

AUTHOR = "Subhajit Guha Thakurta"

DESCRIPTION = "Self-Healing Machine Learning Pipeline using Agentic AI"

# ==============================================================================
# DIRECTORY STRUCTURE
# ==============================================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

TOOLS_DIR = BASE_DIR / "tools"

DATABASE_DIR = BASE_DIR / "database"

MODEL_DIR = BASE_DIR / "models"

SAVED_MODEL_DIR = MODEL_DIR / "saved_models"

SAMPLE_DATA_DIR = BASE_DIR / "sample_data"

LOG_DIR = BASE_DIR / "logs"

VISUALIZATION_DIR = BASE_DIR / "visualization"

PROMPT_DIR = BASE_DIR / "prompts"

# ==============================================================================
# RANDOM SEED
# ==============================================================================

RANDOM_SEED = 42

# ==============================================================================
# DATA GENERATION
# ==============================================================================

DEFAULT_ROWS = 5000

LARGE_DATASET_ROWS = 50000

DATE_START = "2024-01-01"

NUMBER_OF_STORES = 20

NUMBER_OF_PRODUCTS = 60

NUMBER_OF_REGIONS = 5

NUMBER_OF_CATEGORIES = 6

# ==============================================================================
# DATASET FILES
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
# BUSINESS VALUES
# ==============================================================================

REGIONS = [
    "North",
    "South",
    "East",
    "West",
    "Central"
]

PRODUCT_CATEGORIES = [
    "Electronics",
    "Furniture",
    "Clothing",
    "Food",
    "Sports",
    "Books"
]

# ==============================================================================
# SALES GENERATION PARAMETERS
# ==============================================================================

BASE_SALES = 200

BASE_PRICE = 100

PRICE_STD = 20

BASE_MARKETING = 5000

MARKETING_STD = 1200

BASE_COMPETITOR_PRICE = 95

COMPETITOR_STD = 18

BASE_INVENTORY = 400

INVENTORY_STD = 80

BASE_TEMPERATURE = 26

TEMPERATURE_STD = 6

BASE_FOOTFALL = 250

FOOTFALL_STD = 45

DISCOUNT_MIN = 0

DISCOUNT_MAX = 40

# ==============================================================================
# SALES EQUATION WEIGHTS
# ==============================================================================

MARKETING_WEIGHT = 0.035

PRICE_WEIGHT = -1.10

COMPETITOR_WEIGHT = 0.65

INVENTORY_WEIGHT = 0.18

FOOTFALL_WEIGHT = 0.75

TEMPERATURE_WEIGHT = 0.25

HOLIDAY_BONUS = 90

WEEKEND_BONUS = 45

RANDOM_NOISE_STD = 18

# ==============================================================================
# VALIDATION
# ==============================================================================

MAX_ALLOWED_MISSING_PERCENT = 10

MAX_ALLOWED_DUPLICATES = 0

MIN_ALLOWED_PRICE = 0

MIN_ALLOWED_INVENTORY = 0

MIN_ALLOWED_MARKETING = 0

# ==============================================================================
# DRIFT DETECTION
# ==============================================================================

PSI_THRESHOLD = 0.25

MODERATE_PSI = 0.10

# ==============================================================================
# MACHINE LEARNING
# ==============================================================================

TARGET_COLUMN = "Sales"

TEST_SIZE = 0.20

MODEL_VERSION = 1

MODEL_FILE = "sales_forecaster.pkl"

N_ESTIMATORS = 100

LEARNING_RATE = 0.10

MAX_DEPTH = 5

# ==============================================================================
# MODEL PERFORMANCE
# ==============================================================================

MAX_ALLOWED_MAE = 20

MAX_ALLOWED_RMSE = 25

MIN_ALLOWED_R2 = 0.75

# ==============================================================================
# GEMINI CONFIGURATION
# ==============================================================================

LLM_PROVIDER = "gemini"

GEMINI_MODEL = ""

GEMINI_API_KEY = ""

GEMINI_TEMPERATURE = 0.2

MAX_OUTPUT_TOKENS = 2048

# ==============================================================================
# SQLITE
# ==============================================================================

DATABASE_NAME = "pipeline.db"

# ==============================================================================
# STREAMLIT
# ==============================================================================

APP_TITLE = "Self-Healing Agentic AI ML Pipeline"

PAGE_ICON = "🤖"

LAYOUT = "wide"

# ==============================================================================
# EXCEL
# ==============================================================================

DATA_SHEET = "Sales_Data"

METADATA_SHEET = "Metadata"

# ==============================================================================
# LOGGING
# ==============================================================================

LOG_LEVEL = "INFO"

LOG_FILE_NAME = "pipeline.log"

LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

# ==============================================================================
# CREATE DIRECTORIES
# ==============================================================================

DIRECTORIES = [

    DATA_DIR,

    TOOLS_DIR,

    DATABASE_DIR,

    MODEL_DIR,

    SAVED_MODEL_DIR,

    SAMPLE_DATA_DIR,

    LOG_DIR,

    VISUALIZATION_DIR,

    PROMPT_DIR,

]

for directory in DIRECTORIES:

    directory.mkdir(
        parents=True,
        exist_ok=True
    )