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

        return {
            "root_cause":
            response.get(
            "root_cause",
            ""
        ),
        "business_impact":

        response.get(
            "business_impact",
            ""
        ),
        "primary_evidence":

        response.get(
            "primary_evidence",
            []
        )
        }

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
            []
        )

    # ---------------------------------------------------------------------

    def extract_retraining_decision(
        self,
        response: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Return retraining decision.
        """

        

    
        return {
            "recommended_next_step": response.get("recommended_next_step", ""),

    "retrain_required":

        response.get("retrain_required", False)
        }

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

            "business_impact":

    response.get(

        "business_impact",

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

        required_fields = [

    "summary",

    "root_cause",

    "severity",

    "confidence"

]

        missing = [

            field

            for field in required_fields

            if field not in response

        ]

        if missing:

            raise ValueError(

                f"Missing required Gemini response fields: {missing}"

            )

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

    "summary": "Moderate drift detected.",

    "root_cause": "Sales distribution shifted.",

    "business_impact": "Prediction accuracy may decrease.",

    "severity": "HIGH",

    "confidence": 0.96,

    "primary_evidence": [

        "High PSI",

        "RMSE increased"

    ],

    "recommended_next_step": "Retrain Model"

}
    parsed = parser.parse(sample)

    from pprint import pprint

    pprint(parsed)