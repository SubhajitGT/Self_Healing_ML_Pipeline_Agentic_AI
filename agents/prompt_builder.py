"""
===============================================================================
Project : Self-Healing Agentic AI ML Pipeline

File    : prompt_builder.py

Purpose :
Build prompts for Gemini AI using monitoring reports.

Author  : ChatGPT
===============================================================================
"""

from __future__ import annotations

import json
from typing import Dict

# ==============================================================================
# Prompt Builder
# ==============================================================================


class PromptBuilder:
    """
    Build structured prompts for Gemini.

    Responsibilities
    ----------------
    1. Build diagnosis prompt
    2. Build recommendation prompt
    3. Ensure JSON-only responses
    """

    # -------------------------------------------------------------------------

    def __init__(self):

        pass

    # -------------------------------------------------------------------------

    def build_diagnosis_prompt(
        self,
        validation_report: Dict,
        drift_report: Dict,
        performance_report: Dict
    ) -> str:
        """
        Build diagnosis prompt.

        Parameters
        ----------
        validation_report : Dict

        drift_report : Dict

        performance_report : Dict

        Returns
        -------
        str
        """

        prompt = f"""
You are an expert Machine Learning Monitoring Engineer.

Your task is to analyze the monitoring reports and diagnose the
current health of the ML system.

The reports are:

==================================================
VALIDATION REPORT
==================================================

{json.dumps(validation_report, indent=4)}

==================================================
DRIFT REPORT
==================================================

{json.dumps(drift_report, indent=4)}

==================================================
PERFORMANCE REPORT
==================================================

{json.dumps(performance_report, indent=4)}

==================================================

Instructions

1. Analyze every report.

2. Identify possible root causes.

3. Explain business impact.

4. Estimate severity.

5. Estimate confidence.

IMPORTANT

Return ONLY valid JSON.

Do not return markdown.

Do not explain outside JSON.

Return exactly this schema.

{{
    "summary": "",

    "root_cause": "",

    "business_impact": "",

    "severity": "",

    "confidence": 0.0
}}
"""

        return prompt

    # -------------------------------------------------------------------------

    def build_recommendation_prompt(
        self,
        diagnosis: Dict
    ) -> str:
        """
        Build recommendation prompt.
        """

        prompt = f"""
You are an expert MLOps Engineer.

Based on the diagnosis below, provide actionable recommendations.

Diagnosis

{json.dumps(diagnosis, indent=4)}

IMPORTANT

Return ONLY JSON.

Use this schema.

{{
    "recommendations": [

    ],

    "retrain_required": false,

    "priority": "",

    "estimated_impact": ""
}}
"""

        return prompt

    # -------------------------------------------------------------------------

    def build_custom_prompt(
        self,
        title: str,
        data: Dict,
        instructions: str
    ) -> str:
        """
        Build reusable custom prompt.
        """

        prompt = f"""
{title}

==================================================

{json.dumps(data, indent=4)}

==================================================

{instructions}

Return ONLY JSON.
"""

        return prompt

# ==============================================================================
# Standalone Testing
# ==============================================================================

if __name__ == "__main__":

    print("=" * 70)
    print("PROMPT BUILDER TEST")
    print("=" * 70)

    try:

        validation_report = {

            "status": "PASS",

            "missing_columns": [],

            "duplicate_rows": 0,

            "null_percentage": 0.3

        }

        drift_report = {

            "drift_detected": True,

            "overall_drift_score": 0.34,

            "drifted_columns": [

                "Marketing_Spend",

                "Units_Sold"

            ]

        }

        performance_report = {

            "status": "WARNING",

            "mae": 14.52,

            "rmse": 21.81,

            "r2": 0.89

        }

        builder = PromptBuilder()

        prompt = builder.build_diagnosis_prompt(

            validation_report=validation_report,

            drift_report=drift_report,

            performance_report=performance_report

        )

        print()

        print("PROMPT PREVIEW")

        print("-" * 70)

        print(prompt[:1500])

        print()

        print("Prompt Length :", len(prompt))

        print()

        print("=" * 70)

        print("PROMPT BUILDER TEST PASSED")

        print("=" * 70)

    except Exception as error:

        print(error)

        print()

        print("=" * 70)

        print("PROMPT BUILDER TEST FAILED")

        print("=" * 70)

        print(error)