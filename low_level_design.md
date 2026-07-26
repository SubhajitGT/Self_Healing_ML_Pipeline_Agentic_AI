Since this is an **Agentic AI project**, your GitHub should include a **technical architecture** section explaining what happens internally. This is the kind of overview interviewers and recruiters look for because it demonstrates your understanding of the system beyond just the UI.

---

# Low-Level Technical Overview

## End-to-End Pipeline Flow

```text
                    User Uploads Dataset
                             │
                             ▼
                    Streamlit File Upload
                             │
                             ▼
                  Session State Management
                             │
                             ▼
                uploaded_dataframe (Pandas DataFrame)
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
 Data Validation       Model Prediction      Monitoring
        │                    │                    │
        ▼                    ▼                    ▼
 DatasetValidator      FeatureEngineer      DriftDetector
        │                    │                    │
        ▼                    ▼                    ▼
 Validation Report     Production Model     Performance Monitor
        │                    │                    │
        └────────────────────┼────────────────────┘
                             ▼
                      AI Diagnosis Agent
                             │
                    PromptBuilder creates prompt
                             │
                             ▼
                     Google Gemini API
                             │
                             ▼
                   JSON Structured Response
                             │
                             ▼
                     Response Parser
                             │
                             ▼
                      AI Health Report
                             │
                             ▼
                     Self-Healing Engine
                             │
        ┌────────────────────┴────────────────────┐
        ▼                                         ▼
  No Action Required                      Retraining Required
                                                  │
                                                  ▼
                                         Feature Engineering
                                                  │
                                                  ▼
                                            Model Trainer
                                                  │
                                                  ▼
                                           Model Evaluator
                                                  │
                                                  ▼
                                         Promotion Decision
                                                  │
                                                  ▼
                                           Model Manager
                                                  │
                                                  ▼
                                           History Manager
                                                  │
                                                  ▼
                                            SQLite Database
```

---

# Step 1 — Dataset Upload

The user uploads an Excel dataset through the Streamlit interface.

Internally:

```text
Upload Excel

↓

pandas.read_excel()

↓

uploaded_dataframe

↓

st.session_state
```

The dataset is stored in Streamlit Session State so every subsequent page (Validation, Prediction, Monitoring, AI Diagnosis, Self-Healing) works on the same dataframe.

---

# Step 2 — Data Validation

The uploaded dataframe is passed to:

```python
DatasetValidator.validate(dataframe)
```

The validator performs:

* Required column validation
* Missing value detection
* Duplicate row detection
* Schema validation
* Dataset health score calculation

Returns

```python
{
    "status":"PASS",
    "health_score":100,
    "errors":[],
    "warnings":[],
    "summary":{...}
}
```

This report is stored in Session State.

---

# Step 3 — Feature Engineering

Before any prediction or retraining:

```python
FeatureEngineer.prepare_features()
```

Pipeline:

```
Raw Data

↓

Validate Columns

↓

Remove Duplicates

↓

Fill Missing Values

↓

Convert Date Columns

↓

Extract

Year
Month
Day
Quarter
DayOfWeek

↓

Remove Transaction_ID

↓

Return Processed DataFrame
```

Unlike the earlier version of the project, categorical encoding is **not** done here. The raw categorical columns are intentionally preserved.

---

# Step 4 — Model Prediction

Prediction uses the production model.

```
ModelManager

↓

Load latest Pipeline

↓

Pipeline.predict()

↓

Predictions
```

The trained model is an sklearn **Pipeline**:

```
ColumnTransformer

↓

Numeric Imputer

↓

Categorical Imputer

↓

OneHotEncoder(handle_unknown="ignore")

↓

GradientBoostingRegressor
```

Since preprocessing lives inside the pipeline, prediction automatically handles unseen categories and keeps training and inference consistent.

---

# Step 5 — Monitoring

Monitoring consists of three independent analyses.

## Validation

```
Dataset

↓

Validator

↓

Validation Report
```

---

## Drift Detection

A clean reference dataset is generated:

```
SalesDataGenerator

↓

Reference Dataset
```

The uploaded dataset becomes the current dataset.

```
Reference

+

Current

↓

DriftDetector.detect()

↓

Numeric Drift

+

Category Drift
```

Returned report:

```
Drift Detected

Affected Columns

Distribution Changes

New Categories
```

---

## Performance Monitoring

Production metrics

↓

Current metrics

↓

PerformanceMonitor.monitor()

↓

Metric comparison

↓

Performance degradation report

---

# Step 6 — AI Diagnosis

The three reports are combined.

```
Validation Report

+

Drift Report

+

Performance Report

↓

PromptBuilder
```

PromptBuilder converts them into a structured LLM prompt.

Example:

```
Pipeline Health Report

Validation:

...

Drift:

...

Performance:

...

Please provide:

Summary

Severity

Confidence

Diagnosis

Recommendations

Retraining Decision
```

The prompt is sent to:

```
Google Gemini
```

Gemini returns JSON.

Example

```json
{
  "summary":{
      "summary":"Performance degradation detected",
      "severity":"HIGH",
      "confidence":"95%"
  },
  "diagnosis":{...},
  "recommendations":{...},
  "retraining":{...}
}
```

---

# Step 7 — Response Parsing

The raw Gemini JSON is parsed by:

```
ResponseParser
```

It validates:

* Required fields
* JSON format
* Missing keys

and returns a standardized report for the UI.

---

# Step 8 — Self-Healing Engine

This is the autonomous decision-making component.

Workflow:

```
AI Report

↓

Decision

↓

RETRAIN ?

↓

YES
```

Then

```
Feature Engineering

↓

Model Trainer

↓

Candidate Model

↓

Model Evaluator

↓

Candidate Metrics
```

---

# Step 9 — Model Promotion

Candidate metrics are compared with production metrics.

Example

```
Production

MAE = 14.2

Candidate

MAE = 10.8
```

If candidate performance is better:

```
ModelManager.save_model()

↓

sales_forecaster_v2.pkl
```

Otherwise:

```
Production model retained.
```

---

# Step 10 — History Management

Every self-healing execution is saved into SQLite.

Schema

```
Timestamp

Action

Severity

Reason

Candidate Metrics

Production Metrics

Old Version

New Version

Promoted
```

This creates a complete audit trail of every autonomous decision.

---

# Internal Module Dependency Graph

```
Streamlit UI

│

├── DatasetValidator

├── FeatureEngineer

├── Predictor

│      │

│      ▼

│  ModelManager

│

├── DriftDetector

├── PerformanceMonitor

│

├── AIOrchestrator

│      │

│      ▼

│ DiagnosisAgent

│      │

│      ▼

│ PromptBuilder

│      │

│      ▼

│ GeminiClient

│      │

│      ▼

│ ResponseParser

│

└── SelfHealingEngine

        │

        ├── RetrainingEngine

        │      │

        │      ├── FeatureEngineer

        │      ├── ModelTrainer

        │      └── ModelEvaluator

        │

        ├── ModelManager

        └── HistoryManager
```

---

# Why this is "Agentic AI"

This project is more than a traditional ML pipeline because it follows an autonomous perceive–reason–act cycle:

1. **Perceive** – Collects signals from validation, drift detection, and performance monitoring.
2. **Reason** – Uses a large language model (Google Gemini) to synthesize these signals into a diagnosis, severity assessment, and recommended action.
3. **Act** – Executes the recommendation by retraining, evaluating, promoting a better model if appropriate, and recording the decision in persistent history.

Rather than only generating insights, the system can take corrective actions automatically based on its analysis, which is the defining characteristic of an agentic workflow.
