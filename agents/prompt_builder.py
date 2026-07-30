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

You are acting as the AI Diagnosis Agent of a Self-Healing Machine Learning Pipeline.

Think step-by-step internally before answering, but DO NOT expose your reasoning process.

Your task is to:

1. Analyze the validation report first.
   - Determine whether the incoming dataset is structurally valid.
   - Identify missing columns, schema issues, duplicate rows or excessive missing values.

2. Analyze the drift report.
   - Determine whether statistical drift exists.
   - Consider PSI values, drift score, affected columns and overall severity.

3. Analyze the performance report.
   - Determine whether model performance has degraded.
   - Compare MAE, RMSE and R² changes.
   - Determine whether degradation is significant.

4. Correlate all three reports together.

Never make a conclusion from a single report if the other reports contradict it.

For example:

• Validation PASS + High Drift + Performance Healthy
→ Data has changed but model is still stable.

• Validation PASS + High Drift + Performance Critical
→ Drift is probably affecting model quality.

• Validation FAIL
→ Data quality issue has highest priority.

5. Determine the SINGLE most probable root cause.

6. Estimate confidence between 0.0 and 1.0.

Confidence should reflect how strongly the reports support the diagnosis.

7. Keep the business impact concise.

Rules

- Do not invent information.
- Use only the supplied reports.
- If evidence is insufficient, explicitly state that.
- Return valid JSON only.
- Do not include markdown.
- Do not include explanations outside JSON.

Return exactly this schema.

{{
    "summary": "",

    "root_cause": "",

    "business_impact": "",

    "severity": "LOW | MEDIUM | HIGH | CRITICAL",

    "confidence": 0.0,
    "primary_evidence": [
    ],

    "recommended_next_step": ""
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

Based only on the diagnosis below, recommend operational actions.

Prioritize actions that minimize business risk.

Possible actions include:

- Continue Monitoring
- Clean Dataset
- Reject Dataset
- Retrain Model
- Roll Back Previous Model
- Request Human Review

Do not recommend actions that are unsupported by the diagnosis.

Return valid JSON only.

Diagnosis

{json.dumps(diagnosis, indent=4)}

IMPORTANT

Return ONLY JSON.

Use this schema.

{{
    "recommendations": [

    ],

    "primary_action": "",

    "human_intervention_required": false,
    
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