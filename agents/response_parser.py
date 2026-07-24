"""
===============================================================================
Project : Self-Healing Agentic AI ML Pipeline

File    : response_parser.py

Purpose :
Parse structured Gemini responses.

Author  : ChatGPT
===============================================================================
"""

from __future__ import annotations

from typing import Dict, Any


class ResponseParser:
    """
    Parse Gemini JSON response.

    Responsibilities
    ----------------
    1. Extract diagnosis
    2. Extract recommendations
    3. Extract retraining decision
    """

    # ---------------------------------------------------------------------

    def extract_diagnosis(
        self,
        response: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Return diagnosis section.
        """

        return response.get(
            "diagnosis",
            {}
        )

    # ---------------------------------------------------------------------

    def extract_recommendations(
        self,
        response: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Return recommendation section.
        """

        return response.get(
            "recommendations",
            {}
        )

    # ---------------------------------------------------------------------

    def extract_retraining_decision(
        self,
        response: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Return retraining decision.
        """

        return response.get(
            "retraining",
            {}
        )

    # ---------------------------------------------------------------------

    def extract_summary(
        self,
        response: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Return executive summary.
        """

        return {

            "summary":

                response.get(
                    "summary",
                    ""
                ),

            "severity":

                response.get(
                    "severity",
                    "UNKNOWN"
                ),

            "confidence":

                response.get(
                    "confidence",
                    0
                )

        }

    # ---------------------------------------------------------------------

    def parse(
        self,
        response: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Parse complete response.
        """

        return {

            "summary":

                self.extract_summary(
                    response
                ),

            "diagnosis":

                self.extract_diagnosis(
                    response
                ),

            "recommendations":

                self.extract_recommendations(
                    response
                ),

            "retraining":

                self.extract_retraining_decision(
                    response
                )

        }
    
if __name__ == "__main__":

    parser = ResponseParser()

    sample = {

        "summary":
            "Moderate Drift",

        "severity":
            "HIGH",

        "confidence":
            0.96,

        "diagnosis": {

            "root_cause":
                "Sales distribution shifted."

        },

        "recommendations": {

            "actions": [

                "Retrain model",

                "Update reference dataset"

            ]

        },

        "retraining": {

            "required": True,

            "priority": "HIGH"

        }

    }

    parsed = parser.parse(sample)

    from pprint import pprint

    pprint(parsed)