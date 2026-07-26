# 🤖 Self-Healing Agentic AI ML Pipeline

An end-to-end **Agentic AI-powered Self-Healing Machine Learning Pipeline** that continuously monitors production data, detects data quality issues, identifies model drift, performs AI-powered root cause analysis using Google Gemini, and automatically retrains and promotes a better-performing model when required.

---

## 📌 Project Overview

Traditional ML pipelines require manual monitoring and intervention whenever production data quality degrades or model performance deteriorates.

This project demonstrates a **fully automated Self-Healing Machine Learning Pipeline** capable of:

- Uploading production datasets
- Validating incoming data
- Running production predictions
- Detecting data drift
- Monitoring model performance
- Diagnosing issues using an LLM (Google Gemini)
- Automatically retraining models
- Comparing candidate and production models
- Promoting better-performing models
- Maintaining complete self-healing execution history

---

## 🚀 Live Demo

**Application URL**

> **TODO:** Replace after deployment

```
https://<your-streamlit-url>
```

---

## 📸 Screenshots

> **TODO:** Add screenshots after deployment.

### Dashboard

![Dashboard](images/dashboard.png)

### Data Upload

![Upload](images/upload.png)

### Data Validation

![Validation](images/validation.png)

### Prediction

![Prediction](images/prediction.png)

### Monitoring

![Monitoring](images/monitoring.png)

### AI Diagnosis

![Diagnosis](images/diagnosis.png)

### Self-Healing

![Healing](images/healing.png)

---

# Architecture

```
                    Uploaded Dataset
                           │
                           ▼
                 Data Validation Agent
                           │
                           ▼
                 Feature Engineering
                           │
                           ▼
                   ML Prediction
                           │
                           ▼
                 Monitoring Pipeline
            ┌──────────────┴──────────────┐
            ▼                             ▼
     Drift Detection             Performance Monitoring
            │                             │
            └──────────────┬──────────────┘
                           ▼
                  AI Diagnosis Agent
                     (Google Gemini)
                           │
                           ▼
                Self-Healing Decision
                           │
                 ┌─────────┴─────────┐
                 ▼                   ▼
          No Retraining        Retraining Required
                                     │
                                     ▼
                             Train Candidate Model
                                     │
                                     ▼
                          Evaluate Candidate Model
                                     │
                                     ▼
                      Promote Better Model Automatically
                                     │
                                     ▼
                          Update Model Registry
                                     │
                                     ▼
                          Save Execution History
```

---

# Features

## ✅ Data Upload

- Upload Excel datasets
- Automatic schema loading
- Session management

---

## ✅ Data Validation

Checks:

- Missing values
- Duplicate rows
- Required columns
- Data types
- Schema validation
- Health score

---

## ✅ Feature Engineering

Automatic preprocessing including:

- Missing value handling
- Duplicate removal
- Date feature extraction
- Categorical preprocessing
- Production-ready feature pipeline

---

## ✅ Model Training

Model:

- Gradient Boosting Regressor

Training pipeline:

- Train/Test Split
- Scikit-Learn Pipeline
- OneHotEncoder
- Missing value imputation
- Automatic preprocessing

---

## ✅ Model Prediction

- Batch prediction
- Production model loading
- Download prediction results
- Version-aware inference

---

## ✅ Model Monitoring

Includes:

- Dataset validation
- Numerical drift detection
- Categorical drift detection
- Performance monitoring
- Overall health score

---

## ✅ AI Diagnosis

Powered by **Google Gemini**

Analyzes:

- Validation report
- Drift report
- Performance report

Returns:

- Executive summary
- Severity
- Confidence
- Diagnosis
- Recommendations
- Retraining decision

---

## ✅ Self-Healing Engine

Automatically:

- Retrains candidate model
- Evaluates candidate model
- Compares against production
- Promotes best model
- Saves execution history

---

## ✅ Model Versioning

Supports:

- Save models
- Load models
- Delete models
- Latest model retrieval
- Version management

---

## ✅ Execution History

SQLite-backed history including:

- Timestamp
- Action
- Severity
- AI reason
- Model versions
- Candidate metrics
- Production metrics

---

# Technology Stack

| Category | Technology |
|-----------|------------|
| Language | Python 3.11 |
| Frontend | Streamlit |
| ML | Scikit-Learn |
| Data | Pandas, NumPy |
| LLM | Google Gemini |
| Database | SQLite |
| Model Storage | Joblib |
| Visualization | Streamlit |
| Version Control | Git & GitHub |

---

# Project Structure

```
Self_Healing_ML_Pipeline_Agentic_AI/

│
├── agents/
├── data/
├── ml/
├── monitoring/
├── self_healing/
├── streamlit_app/
│
├── models/
│   └── saved_models/
│
├── sample_data/
├── database/
├── utils/
├── config.py
├── requirements.txt
└── README.md
```

---

# Installation

Clone repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Go to project directory

```bash
cd Self_Healing_ML_Pipeline_Agentic_AI
```

Create virtual environment

Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Configuration

Update `config.py`

Example

```python
GEMINI_API_KEY = "YOUR_API_KEY"
```

---

# Run Application

```bash
streamlit run streamlit_app/app.py
```

---

# Workflow

```
Upload Dataset
      │
      ▼
Data Validation
      │
      ▼
Prediction
      │
      ▼
Monitoring
      │
      ▼
AI Diagnosis
      │
      ▼
Self-Healing
```

---

# Sample Dataset

Included sample datasets:

```
sample_data/

sales_normal.xlsx

sales_drift.xlsx

sales_missing_values.xlsx

sales_schema_error.xlsx
```

---

# Future Enhancements

- Docker support
- Kubernetes deployment
- MLflow integration
- Prometheus monitoring
- Grafana dashboards
- CI/CD pipeline
- Multi-model support
- Real-time Kafka streaming
- REST API
- Authentication
- Role-based access control
- Azure/AWS deployment

---

# Author

**Subhajit Guha Thakurta**

LinkedIn

> **TODO:** Add LinkedIn URL

GitHub

> **TODO:** Add GitHub URL

Portfolio

> **TODO:** Add Portfolio URL

---

# License

This project is licensed under the MIT License.

---


## ⭐ If you found this project useful, please consider giving it a Star on GitHub.