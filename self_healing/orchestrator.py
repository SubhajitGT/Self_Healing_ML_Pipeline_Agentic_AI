"""
===============================================================================
Project : Self-Healing Agentic AI ML Pipeline

File    : orchestrator.py

Purpose :
Coordinate the complete self-healing workflow.

Author  : ChatGPT
===============================================================================
"""

from __future__ import annotations

import sys
import logging
from pathlib import Path
from typing import Dict

import pandas as pd

# ==============================================================================
# Add Project Root
# ==============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ==============================================================================

import config

from self_healing.decision_engine import DecisionEngine
from self_healing.retraining_engine import RetrainingEngine
from self_healing.model_promoter import ModelPromoter
from self_healing.history_manager import HistoryManager

# ==============================================================================
# Logging
# ==============================================================================

logger = logging.getLogger("SelfHealingOrchestrator")

logger.setLevel(config.LOG_LEVEL)

formatter = logging.Formatter(config.LOG_FORMAT)

console_handler = logging.StreamHandler(sys.stdout)

console_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(console_handler)

# ==============================================================================
# Self Healing Orchestrator
# ==============================================================================


class SelfHealingOrchestrator:
    """
    Coordinate the complete self-healing workflow.
    """

    # -------------------------------------------------------------------------

    def __init__(self):

        self.decision_engine = DecisionEngine()

        self.retraining_engine = RetrainingEngine()

        self.model_promoter = ModelPromoter()

        self.history_manager = HistoryManager()

    # -------------------------------------------------------------------------

    def should_retrain(
        self,
        decision_report: Dict
    ) -> bool:
        """
        Determine whether retraining is required.
        """

        action = decision_report["decision"]["action"]

        return action == "RETRAIN"

    # -------------------------------------------------------------------------

    def execute(
        self,
        dataframe: pd.DataFrame,
        ai_report: Dict,
        production_metrics: Dict,
        current_version: int = 1
    ) -> Dict:
        """
        Execute complete self-healing workflow.
        """

        logger.info("=" * 60)
        logger.info("Starting Self-Healing Workflow")
        logger.info("=" * 60)

        decision_report = self.decision_engine.execute(

            ai_report

        )

        if not self.should_retrain(

            decision_report

        ):

            logger.info(

                "Retraining not required."

            )

            self.history_manager.save_execution(

                decision_report

            )

            return {

                "workflow_status": "COMPLETED",

                "decision": decision_report,

                "retrained": False,

                "promotion": None

            }

        logger.info(

            "Retraining started."

        )

        candidate = self.retraining_engine.retrain(

            dataframe

        )

        promotion = self.model_promoter.promote(

            candidate_package=candidate,

            production_metrics=production_metrics,

            current_version=current_version

        )

        execution_report = {

            **decision_report,

            **promotion

        }

        self.history_manager.save_execution(

            execution_report

        )

        logger.info(

            "Self-healing completed."

        )

        return {

            "workflow_status": "COMPLETED",

            "decision": decision_report,

            "candidate": candidate,

            "promotion": promotion,

            "retrained": True

        }
    
# ==============================================================================
# Standalone Testing
# ==============================================================================

if __name__ == "__main__":

    from data.generator import SalesDataGenerator

    print("=" * 70)
    print("SELF-HEALING ORCHESTRATOR TEST")
    print("=" * 70)

    try:

        # ---------------------------------------------------------
        # Generate Dataset
        # ---------------------------------------------------------

        generator = SalesDataGenerator(rows=1000)

        dataframe = generator.generate_dataset()

        # ---------------------------------------------------------
        # Sample AI Report
        # ---------------------------------------------------------

        ai_report = {

            "summary": {

                "severity": "HIGH"

            },

            "retraining": {

                "required": True,

                "priority": "HIGH"

            }

        }

        # ---------------------------------------------------------
        # Production Metrics
        # ---------------------------------------------------------

        production_metrics = {

            "mae": 22.4,

            "rmse": 30.7,

            "r2": 0.87

        }

        # ---------------------------------------------------------
        # Execute Self-Healing
        # ---------------------------------------------------------

        orchestrator = SelfHealingOrchestrator()

        result = orchestrator.execute(

            dataframe=dataframe,

            ai_report=ai_report,

            production_metrics=production_metrics,

            current_version=1

        )

        print()

        print("=" * 70)
        print("SELF-HEALING SUMMARY")
        print("=" * 70)

        print(

            "Workflow Status :",

            result["workflow_status"]

        )

        print(

            "Retrained       :",

            result["retrained"]

        )

        if result["promotion"] is not None:

            promotion = result["promotion"]

            print()

            print(

                "Promoted        :",

                promotion["promoted"]

            )

            print(

                "Old Version     :",

                promotion["old_version"]

            )

            print(

                "New Version     :",

                promotion["new_version"]

            )

            print(

                "Reason          :",

                promotion["reason"]

            )

        print()

        print("=" * 70)
        print("SELF-HEALING TEST PASSED")
        print("=" * 70)

    except Exception as error:

        logger.exception(error)

        print()

        print("=" * 70)
        print("SELF-HEALING TEST FAILED")
        print("=" * 70)

        print(error)