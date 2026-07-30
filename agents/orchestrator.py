"""
===============================================================================
Project : Self-Healing Agentic AI ML Pipeline

File    : orchestrator.py

Purpose :
Central AI Orchestrator.

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

from agents.diagnosis_agent import DiagnosisAgent

# ==============================================================================
# Logging
# ==============================================================================

logger = logging.getLogger("AIOrchestrator")

logger.setLevel(config.LOG_LEVEL)

formatter = logging.Formatter(config.LOG_FORMAT)

console_handler = logging.StreamHandler(sys.stdout)

console_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(console_handler)

# ==============================================================================
# AI Orchestrator
# ==============================================================================


class AIOrchestrator:
    """
    Central AI Orchestrator.

    Responsibilities
    ----------------
    1. Call Diagnosis Agent
    2. Parse Gemini response
    3. Return structured AI report
    """

    # ---------------------------------------------------------------------

    def __init__(self):

        self.agent = DiagnosisAgent()


    # ---------------------------------------------------------------------

    def analyze(
        self,
        validation_report: Dict,
        drift_report: Dict,
        performance_report: Dict
    ) -> Dict:
        """
        Execute complete AI workflow.
        """

        logger.info("=" * 60)
        logger.info("Starting AI Analysis")
        logger.info("=" * 60)

        if not validation_report:

            raise ValueError(

        "Validation report cannot be empty."

    )

        if not drift_report:

            raise ValueError(

        "Drift report cannot be empty."

    )

        if not performance_report:

            raise ValueError(

        "Performance report cannot be empty."

    )

        ai_response = self.agent.diagnose(

            validation_report,

            drift_report,

            performance_report

        )

        if "error" in ai_response:

            logger.error(

        ai_response["error"]

    )

            return ai_response

        logger.info(

            "AI analysis completed."

        )
        return ai_response

    # ---------------------------------------------------------------------

    def print_report(
        self,
        report: Dict
    ) -> None:
        """
        Pretty print AI report.
        """
        if "error" in report:

            print()

            print("=" * 70)

            print("AI ERROR")

            print("=" * 70)

            print(report["error"])

            return
        print()

        print("=" * 70)
        print("AI HEALTH REPORT")
        print("=" * 70)

        print()

        summary = report["summary"]

        print(

            f"Summary      : {summary['summary']}"

        )

        print(

            f"Severity     : {summary['severity']}"

        )

        print(

            f"Confidence   : {summary['confidence']}"

        )

        print()

        print("=" * 70)

        print("Diagnosis")

        print("=" * 70)

        for key, value in report["diagnosis"].items():

            print(f"{key:20}: {value}")

        print()

        print("=" * 70)

        print("Recommendations")

        print("=" * 70)

        recommendations = report["recommendations"]

        if isinstance(recommendations, dict):

            actions = recommendations.get(

                "recommendations",

                []

            )

            for action in actions:

                print(f"✔ {action}")

        print()

        print("=" * 70)

        print("Retraining")

        print("=" * 70)

        retraining = report["retraining"]

        for key, value in retraining.items():

            print(f"{key:20}: {value}")

        print()

# ==============================================================================
# Standalone Testing
# ==============================================================================

if __name__ == "__main__":

    from monitoring.validator import DatasetValidator
    from monitoring.drift_detector import DriftDetector
    from monitoring.performance_monitor import PerformanceMonitor

    from data.generator import SalesDataGenerator
    from data.drift_injector import DriftInjector

    print("=" * 70)
    print("AI ORCHESTRATOR TEST")
    print("=" * 70)

    try:

        generator = SalesDataGenerator(rows=1000)

        reference_df = generator.generate_dataset()

        injector = DriftInjector()

        current_df = injector.inject_sudden_drift(

            reference_df.copy()

        )

        validator = DatasetValidator()

        validation_report = validator.validate(

            current_df

        )

        detector = DriftDetector()

        drift_report = detector.detect(

            reference_df,

            current_df

        )

        performance = PerformanceMonitor()

        previous_metrics = {

            "mae": 10.5,

            "rmse": 17.9,

            "r2": 0.95

        }

        current_metrics = {

            "mae": 15.1,

            "rmse": 25.4,

            "r2": 0.85

        }

        performance_report = performance.monitor(

            previous_metrics,

            current_metrics

        )

        orchestrator = AIOrchestrator()

        report = orchestrator.analyze(

            validation_report,

            drift_report,

            performance_report

        )

        orchestrator.print_report(

            report

        )

        print("=" * 70)
        print("AI ORCHESTRATOR TEST PASSED")
        print("=" * 70)

    except Exception as error:

        logger.exception(error)

        print()

        print("=" * 70)
        print("AI ORCHESTRATOR TEST FAILED")
        print("=" * 70)

        print(error)