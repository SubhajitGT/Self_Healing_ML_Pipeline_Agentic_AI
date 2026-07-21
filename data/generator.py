"""
===============================================================================
Project : Self-Healing Agentic AI ML Pipeline

File    : data/generator.py

Purpose :
Generate realistic retail sales data for ML training and testing.

Author  : ChatGPT
===============================================================================
"""
from __future__ import annotations
import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))



import uuid
from datetime import timedelta

import numpy as np
import pandas as pd

import config


class SalesDataGenerator:
    """
    Generates a synthetic retail sales dataset.

    The generated dataset contains:

        • Date Features
        • Numerical Features
        • Categorical Features
        • Target Variable (Sales)

    This dataset is later used for

        • ML Training
        • Drift Injection
        • Validation
        • Streamlit Demo
    """

    def __init__(
        self,
        rows: int = config.DEFAULT_ROWS,
        random_seed: int = config.RANDOM_SEED,
    ):

        self.rows = rows
        self.random_seed = random_seed

        np.random.seed(self.random_seed)

    # -------------------------------------------------------------------------

    def generate_dates(self) -> pd.Series:
        """
        Generate random transaction dates.
        """

        start_date = pd.to_datetime(config.DATE_START)

        random_days = np.random.randint(
            0,
            365,
            self.rows,
        )

        dates = [
            start_date + timedelta(days=int(day))
            for day in random_days
        ]

        return pd.Series(dates)

    # -------------------------------------------------------------------------

    def generate_store_ids(self):

        return np.random.randint(
            1001,
            1001 + config.NUMBER_OF_STORES,
            self.rows,
        )

    # -------------------------------------------------------------------------

    def generate_product_ids(self):

        return np.random.randint(
            5001,
            5001 + config.NUMBER_OF_PRODUCTS,
            self.rows,
        )

    # -------------------------------------------------------------------------

    def generate_regions(self):

        return np.random.choice(
            config.REGIONS,
            self.rows,
        )

    # -------------------------------------------------------------------------

    def generate_categories(self):

        return np.random.choice(
            config.PRODUCT_CATEGORIES,
            self.rows,
        )

    # -------------------------------------------------------------------------

    def generate_price(self):

        return np.round(

            np.random.normal(

                config.BASE_PRICE,

                config.PRICE_STD,

                self.rows,

            ),

            2,

        )

    # -------------------------------------------------------------------------

    def generate_discount(self):

        return np.round(

            np.random.uniform(

                config.DISCOUNT_MIN,

                config.DISCOUNT_MAX,

                self.rows,

            ),

            2,

        )

    # -------------------------------------------------------------------------

    def generate_marketing_spend(self):

        return np.round(

            np.random.normal(

                config.BASE_MARKETING,

                config.MARKETING_STD,

                self.rows,

            ),

            2,

        )

    # -------------------------------------------------------------------------

    def generate_competitor_price(self):

        return np.round(

            np.random.normal(

                config.BASE_COMPETITOR_PRICE,

                config.COMPETITOR_STD,

                self.rows,

            ),

            2,

        )

    # -------------------------------------------------------------------------

    def generate_inventory(self):

        return np.round(

            np.random.normal(

                config.BASE_INVENTORY,

                config.INVENTORY_STD,

                self.rows,

            )

        )

    # -------------------------------------------------------------------------

    def generate_temperature(self):

        return np.round(

            np.random.normal(

                config.BASE_TEMPERATURE,

                config.TEMPERATURE_STD,

                self.rows,

            ),

            2,

        )

    # -------------------------------------------------------------------------

    def generate_customer_footfall(self):

        return np.round(

            np.random.normal(

                config.BASE_FOOTFALL,

                config.FOOTFALL_STD,

                self.rows,

            )

        )

    # -------------------------------------------------------------------------

    def generate_holiday(self):

        return np.random.choice(

            [0, 1],

            self.rows,

            p=[0.90, 0.10],

        )

    # -------------------------------------------------------------------------

    def generate_weekend(
        self,
        dates: pd.Series,
    ):

        return dates.dt.dayofweek.isin(
            [5, 6]
        ).astype(int)

    # -------------------------------------------------------------------------

    def calculate_sales(
        self,
        price,
        marketing,
        competitor,
        inventory,
        footfall,
        temperature,
        holiday,
        weekend,
    ):
        """
        Business equation to calculate Sales.

        The target is intentionally generated using business
        relationships so that the ML model can learn meaningful
        patterns instead of random noise.
        """

        noise = np.random.normal(

            0,

            config.RANDOM_NOISE_STD,

            self.rows,

        )

        sales = (

            config.BASE_SALES

            + marketing * config.MARKETING_WEIGHT

            + competitor * config.COMPETITOR_WEIGHT

            + inventory * config.INVENTORY_WEIGHT

            + footfall * config.FOOTFALL_WEIGHT

            + temperature * config.TEMPERATURE_WEIGHT

            + holiday * config.HOLIDAY_BONUS

            + weekend * config.WEEKEND_BONUS

            + price * config.PRICE_WEIGHT

            + noise

        )

        sales = np.maximum(sales, 0)

        return np.round(sales, 2)

    # -------------------------------------------------------------------------

    def generate_dataset(self) -> pd.DataFrame:

        dates = self.generate_dates()

        price = self.generate_price()

        marketing = self.generate_marketing_spend()

        competitor = self.generate_competitor_price()

        inventory = self.generate_inventory()

        footfall = self.generate_customer_footfall()

        temperature = self.generate_temperature()

        holiday = self.generate_holiday()

        weekend = self.generate_weekend(dates)

        sales = self.calculate_sales(

            price,

            marketing,

            competitor,

            inventory,

            footfall,

            temperature,

            holiday,

            weekend,

        )

        dataframe = pd.DataFrame(

            {

                "Transaction_ID": [

                    str(uuid.uuid4())[:12]

                    for _ in range(self.rows)

                ],

                "Transaction_Date": dates,

                "Store_ID": self.generate_store_ids(),

                "Region": self.generate_regions(),

                "Product_Category": self.generate_categories(),

                "Product_ID": self.generate_product_ids(),

                "Price": price,

                "Discount": self.generate_discount(),

                "Marketing_Spend": marketing,

                "Competitor_Price": competitor,

                "Inventory_Level": inventory,

                "Temperature": temperature,

                "Holiday": holiday,

                "Weekend": weekend,

                "Customer_Footfall": footfall,

                "Sales": sales,

            }

        )

        dataframe.sort_values(

            "Transaction_Date",

            inplace=True,

        )

        dataframe.reset_index(

            drop=True,

            inplace=True,

        )

        return dataframe


# ==============================================================================
# Standalone Execution
# ==============================================================================

if __name__ == "__main__":

    generator = SalesDataGenerator()

    df = generator.generate_dataset()

    print(df.head())

    print()

    print(df.info())

    print()

    print(df.describe())