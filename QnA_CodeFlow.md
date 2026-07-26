I think this is a very good question because how you demonstrate the project is almost as important as the project itself. A recruiter or interviewer usually has 10–15 minutes, so you want to show the most impactful scenarios without overwhelming them.
My recommendation: demonstrate only 4 datasets
These cover nearly every major capability of your application.
Dataset
Demonstrates
Show live?
sales_normal.xlsx
Happy path (validation, prediction, monitoring, AI diagnosis)
✅ Yes
sales_missing_values.xlsx
Data validation catches quality issues
✅ Yes
sales_sudden_drift.xlsx
Drift detection + AI diagnosis + self-healing trigger
✅ Yes
sales_new_category.xlsx
Robust prediction with unseen categories (OneHotEncoder(handle_unknown="ignore"))
✅ Yes

These four tell a complete story.

Keep these in the repository, but don't demo them
You have:
sales_bad_schema.xlsx
sales_duplicate_rows.xlsx
sales_negative_values.xlsx
sales_outliers.xlsx
sales_gradual_drift.xlsx
sales_large_dataset.xlsx
sales_concept_drift.xlsx
I would keep all of them in sample_data/, mention them in the README, but not walk through each one during a demo.
Instead, you can simply say:
"The repository also includes additional datasets covering schema violations, duplicate records, outliers, gradual drift, concept drift, and large-scale datasets for further testing."
That shows breadth without consuming demo time.

Recommended demo flow (10–12 minutes)
Scenario 1 — Happy Path (4–5 minutes)
Use:
sales_normal.xlsx

Show:
Upload
Validation → PASS
Prediction
Monitoring
AI Diagnosis
Self-Healing (if your demo supports it)
This gives the audience confidence that the end-to-end workflow functions.

Scenario 2 — Data Quality Issue (2 minutes)
Use:
sales_missing_values.xlsx

Show:
Validation fails or reports warnings.
Explain that the system prevents poor-quality data from silently entering the pipeline.

Scenario 3 — Drift Detection (2–3 minutes)
Use:
sales_sudden_drift.xlsx

Show:
Drift detection identifies changes.
AI Diagnosis explains the issue.
Self-Healing recommends retraining.
This is the "wow" factor of the project.

Scenario 4 — Production Robustness (1 minute)
Use:
sales_new_category.xlsx

Explain:
"This dataset contains categories not seen during training. Because the production model is built as a Scikit-Learn Pipeline with OneHotEncoder(handle_unknown='ignore'), it can still generate predictions without failing."
This is a strong engineering point that interviewers appreciate.

Datasets to mention only
At the end of the demo, briefly note that the project also includes:
sales_bad_schema.xlsx
sales_duplicate_rows.xlsx
sales_negative_values.xlsx
sales_outliers.xlsx
sales_gradual_drift.xlsx
sales_concept_drift.xlsx
sales_large_dataset.xlsx

You don't need to execute them live.

If you're interviewing
I would present the project in this order:
Problem Statement (1 minute)
"Production ML systems degrade over time due to data quality issues and drift. Manual monitoring is costly and slow."
Architecture (2 minutes)
Show your architecture diagram and explain the agentic workflow.
Live Demo (7–8 minutes)
Use the four datasets above.
Technical Deep Dive (5 minutes, if asked)
Explain:
Scikit-Learn Pipeline
ColumnTransformer
OneHotEncoder(handle_unknown="ignore")
Drift detection
Gemini orchestration
Self-healing decision flow
SQLite history
That sequence highlights both the business value and the technical design without getting bogged down in edge cases.


Yes. If I were the interviewer, I would not be interested in seeing every button click. I would want to understand:
What business problem are you solving?
How does your architecture solve it?
What happens internally?
Why did you design it this way?
What makes it "Agentic AI" instead of a normal ML pipeline?
So your demo should be a technical story, not just a UI walkthrough.

Scenario 1 — Happy Path (5–6 minutes)
Interviewer Question
"Can you explain your project?"
Your Answer
"This project is an end-to-end Self-Healing Agentic AI ML Pipeline. It continuously monitors production data, validates incoming datasets, predicts using the deployed model, detects data drift, monitors model performance, asks an LLM (Google Gemini) to diagnose the pipeline health, and if required, automatically retrains and promotes a better model."
Now start the demo.

Step 1 — Upload Dataset
Dataset:
sales_normal.xlsx

Say:
"This represents today's production sales data."
Explain internally:
Excel

↓

Pandas DataFrame

↓

Streamlit Session State

↓

Available to all pages

Interviewer may ask:
Why Session State?
Answer:
"Without Session State, every page refresh would require uploading the file again. Session State allows the uploaded dataframe to persist across the entire workflow."

Step 2 — Validation
Click:
Run Validation

Explain:
"Before using the dataset, the pipeline validates its quality."
Internally:
DatasetValidator

↓

Required Columns

↓

Schema Validation

↓

Missing Values

↓

Duplicate Rows

↓

Health Score

Show:
PASS

Health Score = 100

Interviewer may ask:
Why validate first?
Answer:
"Because a model should never make predictions on invalid data. Garbage in, garbage out."

Step 3 — Prediction
Click:
Generate Prediction

Explain:
"The production model is loaded from disk using ModelManager."
Internally:
ModelManager

↓

Load Pipeline

↓

Pipeline.predict()

Then explain:
"The model itself is a Scikit-Learn Pipeline."
Draw:
Input

↓

ColumnTransformer

↓

Numeric Imputer

↓

Categorical Imputer

↓

OneHotEncoder

↓

Gradient Boosting

↓

Prediction

Interviewer may ask:
Why Pipeline?
Answer:
"Earlier I manually encoded categories and prediction failed whenever a new category appeared. Moving preprocessing inside the Pipeline guarantees identical transformations during training and inference."
This answer is very strong technically.

Step 4 — Monitoring
Click:
Run Monitoring

Explain:
Monitoring has three components.
Validation
Already done.

Drift Detection
Explain:
Reference Dataset

+

Current Dataset

↓

DriftDetector

It compares
Numeric distributions
Category distributions
Show:
No drift detected.


Performance Monitoring
Explain:
Previous Metrics

↓

Current Metrics

↓

Comparison

↓

Health Report


Step 5 — AI Diagnosis
Click
Run AI Diagnosis

Explain:
Three reports are combined.
Validation

+

Drift

+

Performance

↓

Prompt Builder

Prompt Builder creates:
Validation Summary

Drift Summary

Performance Summary

↓

Gemini

Gemini returns JSON.
Explain:
"Instead of asking Gemini to return free text, I force it to return structured JSON. This makes the output machine-readable."
Interviewer usually likes this answer.

Step 6 — Self Healing
Explain:
Gemini

↓

Retraining Required?

↓

YES

↓

Retrain Candidate

↓

Evaluate Candidate

↓

Compare

↓

Promote

Say:
"The pipeline doesn't blindly replace the production model."
Instead
Candidate

vs

Production

Only better model gets promoted.
This is very important.

Scenario 2 — Missing Values
Dataset
sales_missing_values.xlsx

Say
"Suppose production sends corrupted data."
Upload.
Validation.
Show
Missing Values

Explain:
"The system immediately detects data quality degradation before prediction."
Interviewer:
Why not automatically fill them?
Answer:
"That depends on business policy. Some missing values are acceptable, others indicate upstream ETL failures. I expose the issue first instead of silently hiding it."
Excellent answer.

Scenario 3 — Drift
Dataset
sales_sudden_drift.xlsx

Explain:
"The schema is correct, but customer behaviour changed."
Validation
↓
PASS
Prediction
↓
Works
Monitoring
↓
Drift
↓
Detected
Then AI Diagnosis.
Gemini says
HIGH

Retraining Recommended

Now explain:
"This demonstrates why validation alone isn't sufficient. The data is syntactically correct but statistically different."
That distinction impresses interviewers.

Scenario 4 — New Categories
Dataset
sales_new_category.xlsx

Say
"This dataset contains categories never seen during training."
Old approach
pd.get_dummies()

↓

Crash

Current approach
Pipeline

↓

OneHotEncoder(handle_unknown="ignore")

↓

Prediction succeeds

This showcases a practical engineering improvement.

Scenario 5 — Self-Healing
This is your strongest feature.
Explain slowly.
Monitoring

↓

AI Diagnosis

↓

Decision

↓

Retraining Engine

↓

Feature Engineering

↓

Training

↓

Evaluation

↓

Promotion

↓

History

Explain:
"Every self-healing decision is persisted."
Open SQLite History.
Show
Timestamp

Action

Old Version

New Version

Metrics

Reason

Interviewer:
Why store history?
Answer:
"For auditability, rollback, governance, and understanding why a model was promoted."

Questions they'll likely ask
Why Gemini?
Answer:
"Traditional rule-based systems can detect threshold violations but struggle to synthesize multiple signals. Gemini combines validation, drift, and performance reports into a coherent diagnosis and actionable recommendation."

Why Gradient Boosting?
Answer:
"For tabular regression it provides strong performance with relatively little tuning, making it suitable for demonstrating the self-healing workflow."

Why SQLite?
Answer:
"The project requires lightweight persistent storage for execution history. SQLite is sufficient for a single-node demo and can be replaced with PostgreSQL or another database in production."

Why Streamlit?
Answer:
"It provides a quick way to expose the end-to-end workflow so the focus remains on the ML pipeline and agentic automation rather than front-end development."

Why is this Agentic AI?
This is perhaps the most important question.
Answer:
"An agent doesn't just generate text—it perceives the environment, reasons about the situation, and takes actions. My pipeline perceives validation, drift, and performance signals, reasons over them using Gemini, and then executes actions such as retraining, model evaluation, promotion, and history logging. That's why I classify it as an agentic workflow rather than a conventional ML monitoring dashboard."

One suggestion
Given the amount of engineering you've put into this project, I'd also prepare a 15–20 interview Q&A document specific to your implementation. It would cover questions like:
Why use a Scikit-Learn Pipeline instead of manual preprocessing?
Why compare candidate and production models before promotion?
How would you replace the synthetic reference dataset in a real production environment?
How would you extend the design to use MLflow, Kafka, Airflow, or Kubernetes?
Those are exactly the kinds of follow-up questions interviewers tend to ask after seeing a project like yours.

