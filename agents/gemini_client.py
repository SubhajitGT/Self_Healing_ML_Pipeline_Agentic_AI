"""
===============================================================================
Project : Self-Healing Agentic AI ML Pipeline

File    : gemini_client.py

Purpose :
Central Gemini Client for all AI agents.

Author  : ChatGPT
===============================================================================
"""

from __future__ import annotations

import sys
import json
import logging
from pathlib import Path
from typing import Dict, Any

# ==============================================================================
# Add Project Root
# ==============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ==============================================================================

import config

from google import genai

# ==============================================================================
# Logging
# ==============================================================================

logger = logging.getLogger("GeminiClient")

logger.setLevel(config.LOG_LEVEL)

formatter = logging.Formatter(config.LOG_FORMAT)

console_handler = logging.StreamHandler(sys.stdout)

console_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(console_handler)

# ==============================================================================
# Gemini Client
# ==============================================================================


class GeminiClient:
    """
    Central Gemini Client.

    Responsibilities
    ----------------
    1. Connect to Gemini
    2. Send Prompt
    3. Receive Response
    4. Parse JSON
    """

    # -------------------------------------------------------------------------

    def __init__(self):

        if not config.GEMINI_API_KEY:

            raise ValueError(

                "GEMINI_API_KEY not configured in config.py"

            )

        self.client = genai.Client(

            api_key=config.GEMINI_API_KEY

        )

        self.model = config.GEMINI_MODEL

        logger.info(

            "Gemini Client initialized."

        )

    # -------------------------------------------------------------------------

    def generate_response(
        self,
        prompt: str
    ) -> str:
        """
        Generate response from Gemini.

        Parameters
        ----------
        prompt : str

        Returns
        -------
        str
        """

        logger.info("=" * 60)

        logger.info("Sending Prompt to Gemini")

        logger.info("=" * 60)

        response = self.client.models.generate_content(

            model=self.model,

            contents=prompt

        )

        text = response.text

        logger.info(

            "Response received."

        )

        return text

    # -------------------------------------------------------------------------

    def generate_json_response(
        self,
        prompt: str
    ) -> Dict[str, Any]:
        """
        Generate JSON response.

        Parameters
        ----------
        prompt : str

        Returns
        -------
        Dict
        """

        response_text = self.generate_response(

            prompt

        )

        try:

            return json.loads(

                response_text

            )

        except Exception:

            logger.warning(

                "Gemini returned non-JSON response."

            )

            return {

                "raw_response": response_text

            }