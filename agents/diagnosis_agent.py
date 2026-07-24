"""
===============================================================================
Project : Self-Healing Agentic AI ML Pipeline

File    : diagnosis_agent.py

Purpose :
AI-powered diagnosis of ML pipeline health.

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

from agents.gemini_client import GeminiClient
from agents.prompt_builder import PromptBuilder

# ==============================================================================
# Logging
# ==============================================================================

logger = logging.getLogger("DiagnosisAgent")

logger.setLevel(config.LOG_LEVEL)

formatter = logging.Formatter(config.LOG_FORMAT)

console_handler = logging.StreamHandler(sys.stdout)

console_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(console_handler)

# ==============================================================================
# Diagnosis Agent
# ==============================================================================


class DiagnosisAgent:
    """
    AI Diagnosis Agent.

    Responsibilities
    ----------------
    1. Build diagnosis prompt
    2. Send prompt to Gemini
    3. Return structured diagnosis
    """

    # -------------------------------------------------------------------------

    def __init__(self):

        self.prompt_builder = PromptBuilder()

        self.gemini = GeminiClient()

    # -------------------------------------------------------------------------

    def diagnose(
        self,
        validation_report: Dict,
        drift_report: Dict,
        performance_report: Dict
    ) -> Dict:
        """
        Diagnose ML pipeline health.

        Parameters
        ----------
        validation_report

        drift_report

        performance_report

        Returns
        -------
        Dict
        """

        logger.info("=" * 60)

        logger.info("Starting AI Diagnosis")

        logger.info("=" * 60)

        prompt = self.prompt_builder.build_diagnosis_prompt(

            validation_report,

            drift_report,

            performance_report

        )

        diagnosis = self.gemini.generate_json_response(

            prompt

        )

        logger.info(

            "Diagnosis completed."

        )

        return diagnosis

    # -------------------------------------------------------------------------

    def pretty_print(
        self,
        diagnosis: Dict
    ) -> None:
        """
        Print diagnosis nicely.
        """

        print()

        print("=" * 70)

        print("AI DIAGNOSIS")

        print("=" * 70)

        print()

        for key, value in diagnosis.items():

            print(f"{key:20}: {value}")

        print()