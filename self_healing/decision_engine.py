"""
===============================================================================
Project : Self-Healing Agentic AI ML Pipeline

File    : decision_engine.py

Purpose :
Decide what self-healing action should be executed.

Author  : ChatGPT
===============================================================================
"""

from __future__ import annotations

import sys
import logging
from pathlib import Path
from typing import Dict

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

logger = logging.getLogger("DecisionEngine")

logger.setLevel(config.LOG_LEVEL)

formatter = logging.Formatter(config.LOG_FORMAT)

console_handler = logging.StreamHandler(sys.stdout)

console_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(console_handler)

# ==============================================================================
# Decision Engine
# ==============================================================================


class DecisionEngine:
    """
    Rule-based Self-Healing Decision Engine.

    Responsibilities
    ----------------
    1. Analyze AI report
    2. Decide action
    3. Assign priority
    """

    # ---------------------------------------------------------------------

    def __init__(self):

        self.rules = {

            "LOW": {

                "action": "KEEP_MODEL",

                "priority": 3

            },

            "MEDIUM": {

                "action": "MONITOR",

                "priority": 2

            },

            "HIGH": {

                "action": "RETRAIN",

                "priority": 1

            },

            "CRITICAL": {

                "action": "RETRAIN",

                "priority": 0

            }

        }

    # ---------------------------------------------------------------------

    def get_severity(
        self,
        ai_report: Dict
    ) -> str:
        """
        Extract severity from AI report.
        """

        summary = ai_report.get(

            "summary",

            {}

        )

        severity = summary.get(

            "severity",

            "LOW"

        )

        return severity.upper()

    # ---------------------------------------------------------------------

    def get_retraining_flag(
        self,
        ai_report: Dict
    ) -> bool:
        """
        Check whether AI recommends retraining.
        """

        retraining = ai_report.get(

            "retraining",

            {}

        )

        return retraining.get(

            "required",

            False

        )

    # ---------------------------------------------------------------------

    def get_priority(
        self,
        severity: str
    ) -> int:
        """
        Return priority from rules.
        """

        return self.rules.get(

            severity,

            self.rules["LOW"]

        )["priority"]

    # ---------------------------------------------------------------------

    def get_default_action(
        self,
        severity: str
    ) -> str:
        """
        Return default action.
        """

        return self.rules.get(

            severity,

            self.rules["LOW"]

        )["action"]
    
    # ---------------------------------------------------------------------

    def decide(
        self,
        ai_report: Dict
    ) -> Dict:
        """
        Decide the self-healing action.

        Parameters
        ----------
        ai_report : Dict

        Returns
        -------
        Dict
        """

        logger.info("=" * 60)
        logger.info("Evaluating Self-Healing Decision")
        logger.info("=" * 60)

        severity = self.get_severity(
            ai_report
        )

        retrain_required = self.get_retraining_flag(
            ai_report
        )

        action = self.get_default_action(
            severity
        )

        priority = self.get_priority(
            severity
        )

        reason = ""

        # ---------------------------------------------------------
        # AI Recommendation Override
        # ---------------------------------------------------------

        if retrain_required:

            action = "RETRAIN"

            reason = (

                "Gemini recommends retraining."

            )

        else:

            if action == "KEEP_MODEL":

                reason = (

                    "Model is healthy."

                )

            elif action == "MONITOR":

                reason = (

                    "Continue monitoring model."

                )

            elif action == "RETRAIN":

                reason = (

                    "High severity detected."

                )

        decision = {

            "severity": severity,

            "action": action,

            "priority": priority,

            "retrain_required": retrain_required,

            "reason": reason

        }

        logger.info(

            "Decision : %s",

            action

        )

        return decision

    # ---------------------------------------------------------------------

    def generate_decision_report(
        self,
        ai_report: Dict
    ) -> Dict:
        """
        Generate complete decision report.
        """

        from datetime import datetime

        decision = self.decide(

            ai_report

        )

        report = {

            "timestamp":

                datetime.now().isoformat(),

            "decision":

                decision,

            "ai_summary":

                ai_report.get(

                    "summary",

                    {}

                )

        }

        return report
    
    # ---------------------------------------------------------------------

    def execute(
        self,
        ai_report: Dict
    ) -> Dict:
        """
        Execute decision engine.
        """

        return self.generate_decision_report(

            ai_report

        )
    
# ==============================================================================
# Standalone Testing
# ==============================================================================

if __name__ == "__main__":

    print("=" * 70)
    print("DECISION ENGINE TEST")
    print("=" * 70)

    sample_report = {

        "summary": {

            "severity": "HIGH"

        },

        "retraining": {

            "required": True,

            "priority": "HIGH"

        }

    }

    try:

        engine = DecisionEngine()

        report = engine.execute(

            sample_report

        )

        print()

        print("=" * 70)
        print("DECISION REPORT")
        print("=" * 70)

        decision = report["decision"]

        print(

            "Severity           :",

            decision["severity"]

        )

        print(

            "Action             :",

            decision["action"]

        )

        print(

            "Priority           :",

            decision["priority"]

        )

        print(

            "Retrain Required   :",

            decision["retrain_required"]

        )

        print(

            "Reason             :",

            decision["reason"]

        )

        print()

        print("=" * 70)
        print("DECISION ENGINE TEST PASSED")
        print("=" * 70)

    except Exception as error:

        logger.exception(error)

        print()

        print("=" * 70)
        print("DECISION ENGINE TEST FAILED")
        print("=" * 70)

        print(error)