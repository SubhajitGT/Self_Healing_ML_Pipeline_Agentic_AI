"""
===============================================================================
Project : Self-Healing Agentic AI ML Pipeline

File    : model_promoter.py

Purpose :
Compare candidate and production models and promote the better model.

Author  : ChatGPT
===============================================================================
"""

from __future__ import annotations

import sys
import logging
from pathlib import Path
from typing import Dict
from ml.model_manager import ModelManager

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

logger = logging.getLogger("ModelPromoter")

logger.setLevel(config.LOG_LEVEL)

formatter = logging.Formatter(config.LOG_FORMAT)

console_handler = logging.StreamHandler(sys.stdout)

console_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(console_handler)

# ==============================================================================
# Model Promoter
# ==============================================================================


class ModelPromoter:
    """
    Compare production and candidate models.

    Responsibilities
    ----------------
    1. Compare metrics
    2. Decide promotion
    3. Generate promotion report
    """

    # -------------------------------------------------------------------------

    def __init__(self):

        pass

    # -------------------------------------------------------------------------

    def compare_metrics(
        self,
        production_metrics: Dict,
        candidate_metrics: Dict
    ) -> Dict:
        """
        Compare production and candidate metrics.
        """

        logger.info("=" * 60)
        logger.info("Comparing Model Metrics")
        logger.info("=" * 60)

        comparison = {

            "r2":

                candidate_metrics["r2"] >

                production_metrics["r2"],

            "rmse":

                candidate_metrics["rmse"] <

                production_metrics["rmse"],

            "mae":

                candidate_metrics["mae"] <

                production_metrics["mae"]

        }

        logger.info(

            "Metric comparison completed."

        )

        return comparison

    # -------------------------------------------------------------------------

    def is_candidate_better(
        self,
        comparison: Dict
    ) -> bool:
        """
        Candidate must win at least
        two out of three metrics.
        """

        wins = sum(

            comparison.values()

        )

        logger.info(

            "Candidate Wins : %d / 3",

            wins

        )

        return wins >= 2

    # -------------------------------------------------------------------------

    def promotion_decision(
        self,
        production_metrics: Dict,
        candidate_metrics: Dict
    ) -> Dict:
        """
        Decide whether candidate should
        become production model.
        """

        comparison = self.compare_metrics(

            production_metrics,

            candidate_metrics

        )

        promote = self.is_candidate_better(

            comparison

        )

        if promote:

            reason = (

                "Candidate outperformed production model."

            )

        else:

            reason = (

                "Production model remains better."

            )

        report = {

            "promote": promote,

            "comparison": comparison,

            "reason": reason

        }

        logger.info(

            "Promotion Decision : %s",

            "PROMOTE"

            if promote

            else

            "KEEP CURRENT"

        )

        return report
    
    # -------------------------------------------------------------------------

    def promote(
        self,
        candidate_package: Dict,
        production_metrics: Dict,
        current_version: int = 1
    ) -> Dict:
        """
        Promote candidate model if it outperforms
        the production model.

        Parameters
        ----------
        candidate_package : Dict

        production_metrics : Dict

        current_version : int

        Returns
        -------
        Dict
        """

        logger.info("=" * 60)
        logger.info("Starting Model Promotion")
        logger.info("=" * 60)

        candidate_metrics = candidate_package[
            "candidate_metrics"
        ]

        report = self.promotion_decision(

            production_metrics,

            candidate_metrics

        )

        promoted = report["promote"]

        new_version = current_version

        if promoted:

            new_version = current_version + 1

            logger.info(

                "Saving candidate as Version %d",

                new_version

            )

            self.model_manager.save_model(

                candidate_package["candidate_model"],

                version=new_version

            )

        return {

            "promoted": promoted,

            "old_version": current_version,

            "new_version": new_version,

            "reason": report["reason"],

            "comparison": report["comparison"],

            "candidate_metrics": candidate_metrics,

            "production_metrics": production_metrics

        }

# ==============================================================================
# Standalone Testing
# ==============================================================================

if __name__ == "__main__":

    from data.generator import SalesDataGenerator

    from self_healing.retraining_engine import RetrainingEngine

    print("=" * 70)
    print("MODEL PROMOTER TEST")
    print("=" * 70)

    try:

        # ---------------------------------------------------------
        # Generate Dataset
        # ---------------------------------------------------------

        generator = SalesDataGenerator(

            rows=1000

        )

        dataframe = generator.generate_dataset()

        # ---------------------------------------------------------
        # Candidate Model
        # ---------------------------------------------------------

        engine = RetrainingEngine()

        candidate = engine.retrain(

            dataframe

        )

        # ---------------------------------------------------------
        # Production Metrics
        # ---------------------------------------------------------

        production_metrics = {

            "mae": 20.5,

            "rmse": 30.8,

            "r2": 0.88

        }

        # ---------------------------------------------------------
        # Promotion
        # ---------------------------------------------------------

        promoter = ModelPromoter()

        result = promoter.promote(

            candidate_package=candidate,

            production_metrics=production_metrics,

            current_version=1

        )

        print()

        print("=" * 70)
        print("PROMOTION REPORT")
        print("=" * 70)

        print(

            "Promoted        :",

            result["promoted"]

        )

        print(

            "Old Version     :",

            result["old_version"]

        )

        print(

            "New Version     :",

            result["new_version"]

        )

        print(

            "Reason          :",

            result["reason"]

        )

        print()

        print("Metric Comparison")

        print("-" * 60)

        for metric, status in result["comparison"].items():

            print(

                f"{metric:10} :",

                status

            )

        print()

        print("=" * 70)
        print("MODEL PROMOTER TEST PASSED")
        print("=" * 70)

    except Exception as error:

        logger.exception(error)

        print()

        print("=" * 70)
        print("MODEL PROMOTER TEST FAILED")
        print("=" * 70)

        print(error)