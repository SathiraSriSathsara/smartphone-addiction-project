# AGENTS.md

## Project Overview

This repository contains the implementation of a university Computational Intelligence project for:

**Project:** Smartphone Addiction Prediction  
**Module:** CIS6005 Computational Intelligence  
**Assessment:** WRIT1  
**Kaggle Competition:** Predicting Smartphone Addiction — Playground Series Season 6 Episode 8  
**Student ID:** 20302367  

The system uses a trained LightGBM machine-learning model to estimate the probability of smartphone addiction from user-provided behavioural and demographic information.

The final project includes:

- Exploratory data analysis
- Model comparison
- Cross-validation
- Kaggle submission generation
- Saved production model
- FastAPI prediction service
- Responsive web application
- Automated tests
- Docker deployment
- Technical documentation

---

## Primary Objective

Develop a reliable, explainable and usable machine-learning application that:

1. Accepts smartphone-usage information from a user.
2. Validates the supplied information.
3. Applies the same feature engineering and preprocessing used during training.
4. Generates an addiction-risk probability using the saved model.
5. Presents the result clearly and responsibly.
6. Makes no medical or clinical claims.

---

## Repository Structure

Expected project structure:

```text
smartphone-addiction-project/
├── api/
├── data/
├── docs/
├── models/
├── notebooks/
├── outputs/
├── screenshots/
├── src/
├── tests/
├── web/
├── .env.example
├── .gitignore
├── AGENTS.md
├── Dockerfile
├── docker-compose.yml
├── pytest.ini
├── README.md
└── requirements.txt
```

Important paths:

```text
models/smartphone_addiction_model.joblib
models/model_metadata.json
models/environment.json
models/requirements-model.txt

notebooks/CIS6005_Smartphone_Addiction_Full_Notebook.ipynb

outputs/results/model_comparison.csv
outputs/results/cross_validation_results.csv
outputs/results/feature_importance.csv

outputs/submissions/submission_lightgbm.csv
```

---

## Development Workflow

Work one phase at a time.

For every major phase:

1. Inspect the existing implementation.
2. Read all files relevant to the task.
3. Propose a concise implementation plan.
4. Modify only files required for the current phase.
5. Run appropriate tests and validation commands.
6. Report:

   * files created
   * files modified
   * commands executed
   * tests performed
   * actual results
   * unresolved issues
7. Stop after the requested phase is complete.
8. Do not start the next phase automatically.

Do not make unrelated improvements during a scoped task.

---

## Critical Rules

### Data and model integrity

* Never invent dataset columns.
* Never rename model features unless the saved model and metadata are updated consistently.
* Inspect the actual metadata and saved pipeline before creating request schemas.
* Do not retrain or overwrite the model unless explicitly requested.
* Do not modify the original Kaggle data files.
* Do not modify the executed notebook unless explicitly requested.
* Do not fabricate model scores, Kaggle scores, metrics or experiment results.
* Do not claim that code was executed unless it ran successfully.
* Do not claim tests passed unless they were actually executed.
* Preserve feature order where the model requires it.
* Never include the Kaggle `id` column as a user prediction feature.
* Use `predict_proba` for addiction probability when supported.

### Preprocessing consistency

The API must reproduce the training workflow exactly:

```text
Raw input
    ↓
Feature engineering
    ↓
Missing-value handling
    ↓
Categorical encoding
    ↓
Saved LightGBM pipeline
    ↓
Probability prediction
```

* Use the complete saved pipeline whenever possible.
* Do not manually reproduce preprocessing already stored inside the pipeline.
* Reuse shared feature-engineering functions.
* Do not implement separate feature logic in the frontend and backend.
* Prevent train/inference preprocessing mismatches.
* Handle missing values exactly as the trained pipeline expects.
* Handle unknown categories safely.

### Reproducibility

* Use `random_state=42` for reproducible experiments.
* Record package versions.
* Respect `models/environment.json`.
* Pin model-runtime dependencies where compatibility matters.
* Use paths relative to the repository root.
* Avoid machine-specific absolute paths.
* Ensure commands work from the repository root.

---

## Academic Integrity

This is assessed university work.

* Generated code is a development aid and must remain understandable to the student.
* Do not copy Kaggle notebooks or third-party code without attribution.
* Record all external sources, notebooks and implementations consulted.
* Do not generate fake academic citations.
* Do not generate fake screenshots.
* Do not generate fake experimental results.
* Do not conceal AI-assisted work where disclosure is required.
* Preserve the student's ability to explain:

  * code flow
  * model inputs
  * model outputs
  * preprocessing
  * feature engineering
  * evaluation metrics
  * validation strategy
  * API behaviour
  * application limitations

Do not create final report claims that are unsupported by repository evidence.

---

## Machine-Learning Requirements

The trained model currently selected is expected to be LightGBM.

Verified Kaggle information:

```text
Competition: Predicting Smartphone Addiction
Competition ID: playground-series-s6e8
Public leaderboard score: 0.96189
```

The application must not claim that the leaderboard score represents clinical accuracy.

Before exposing model information:

* Read `model_metadata.json`.
* Read `environment.json`.
* Inspect the loaded pipeline.
* Confirm model classes.
* Confirm `predict_proba` support.
* Confirm the positive class ordering.
* Confirm exact raw input features.
* Confirm engineered features.

Do not assume class index `1` without verifying `model.classes_`.

---

## Validation Requirements

Use Pydantic validation for API requests.

Validation must include:

* Required fields
* Correct data types
* Finite numeric values
* Sensible minimum and maximum values
* Allowed categorical values
* Clear error messages

Do not accept:

* NaN
* Infinity
* Negative durations
* Impossible ages
* Arbitrary categorical values
* Extra fields unless explicitly supported

Return standard HTTP status codes:

```text
200 — Successful request
400 — Invalid business-level request
404 — Resource not found
422 — Request validation failure
500 — Unexpected server/model failure
503 — Model unavailable
```

Never expose stack traces or local file paths in production responses.

---

## Prediction Response

The prediction endpoint should return a structure similar to:

```json
{
  "predicted_class": 1,
  "addiction_probability": 0.824,
  "non_addiction_probability": 0.176,
  "risk_level": "High",
  "risk_message": "The model detected a high predicted likelihood based on the supplied usage pattern.",
  "model_version": "1.0.0",
  "disclaimer": "This result is generated by an educational machine-learning model and is not a medical diagnosis."
}
```

Risk thresholds:

```text
Low:       probability < 0.35
Moderate:  0.35 <= probability < 0.65
High:      probability >= 0.65
```

These thresholds are application display thresholds, not clinical thresholds.

---

## API Requirements

Use FastAPI.

Expected endpoints:

```text
GET  /
GET  /api/health
GET  /api/model/info
GET  /api/model/schema
POST /api/predict
```

The application should:

* Load the model once at startup.
* Avoid loading the model for every request.
* Use dependency injection where appropriate.
* Use Pydantic request and response schemas.
* Configure CORS through environment variables.
* Include API documentation.
* Include structured logging.
* Return consistent JSON error responses.

Do not expose:

* Absolute model paths
* Internal stack traces
* Secrets
* Full environment details
* Raw training data

---

## Frontend Requirements

Use plain HTML, CSS and JavaScript unless explicitly instructed otherwise.

Pages may include:

```text
web/index.html
web/predict.html
web/about.html
web/model.html
web/disclaimer.html
```

Design direction:

* Teal/dark navy visual identity
* Coral primary action button
* Clean, modern layout
* Responsive design
* Accessible contrast
* Keyboard-friendly controls
* Clear loading and error states
* Educational disclaimer
* No login or registration requirement

The landing-page CTA should navigate to the prediction page.

The prediction form must use actual model features.

Do not hardcode guessed fields when `/api/model/schema` can provide them.

---

## Explainability Rules

Do not fabricate individual contributing factors.

Global feature importance is not the same as local prediction explanation.

If explainability is implemented:

* Use a technically valid method such as SHAP where compatible.
* Explain one prediction using transformed features.
* Map encoded features back to readable names.
* Label results as model influences, not causes.
* Do not convert SHAP values into fake causal percentages.
* Provide a fallback if explanation generation fails.

Acceptable wording:

```text
Model factors influencing this prediction
```

Avoid wording such as:

```text
These factors caused the addiction
```

---

## Ethical and Safety Requirements

The application concerns behavioural and potentially sensitive information.

Always include:

* Educational-use disclaimer
* Non-diagnostic disclaimer
* Data-minimisation principles
* Privacy-focused wording
* Bias and limitation disclosure

The application must not:

* Diagnose smartphone addiction
* Recommend medication
* Replace healthcare professionals
* Label users as medically addicted
* Store personal data without explicit implementation and disclosure
* Present probabilities as certainty

Preferred wording:

```text
This application is an educational machine-learning prototype.
It does not provide a medical or psychological diagnosis.
```

---

## Testing Requirements

Use `pytest`.

Expected tests include:

```text
tests/test_health.py
tests/test_model_loader.py
tests/test_feature_engineering.py
tests/test_prediction.py
tests/test_validation.py
```

Test at least:

* Health endpoint
* Root endpoint
* Model loading
* Missing model file behaviour
* Feature engineering
* Input immutability
* Valid prediction
* Missing required field
* Invalid category
* Out-of-range numeric value
* Probability range
* Required response fields
* Low/moderate/high risk mapping
* Unexpected prediction failure

At least one integration test should use the real saved model.

Run from the repository root:

```bash
pytest -v
```

Also run:

```bash
python -m compileall api src
```

Do not remove failing tests to make the suite pass.

---

## Security Requirements

* Keep secrets in environment variables.
* Never commit `.env`.
* Restrict CORS.
* Validate request payloads.
* Avoid arbitrary file uploads unless required.
* Do not use `eval()` or `exec()`.
* Do not deserialize user-supplied model files.
* Load only the trusted local model.
* Do not expose sensitive filesystem information.
* Use safe logging.
* Avoid logging complete personal input payloads.
* Add request size limits where appropriate.
* Run the container as a non-root user where practical.

---

## Environment Configuration

Expected environment variables:

```text
APP_NAME=SmartHabit API
APP_VERSION=1.0.0
ENVIRONMENT=development
MODEL_PATH=models/smartphone_addiction_model.joblib
METADATA_PATH=models/model_metadata.json
ALLOWED_ORIGINS=http://localhost:5500,http://127.0.0.1:5500
```

Document them in `.env.example`.

Never commit real secrets.

---

## Git Rules

Before each phase:

```bash
git status
```

After a successful phase:

```bash
git add .
git commit -m "<clear phase description>"
```

Do not:

* Rewrite Git history
* Force-push
* Delete unrelated files
* Commit raw virtual environments
* Commit caches
* Commit `.env`
* Commit temporary model files
* Commit large generated files unless required

---

## Files That Must Not Be Modified Without Explicit Permission

```text
data/train.csv
data/test.csv
data/sample_submission.csv

models/smartphone_addiction_model.joblib

notebooks/CIS6005_Smartphone_Addiction_Full_Notebook.ipynb

outputs/submissions/submission_lightgbm.csv
```

These files are evidence of the original training and Kaggle workflow.

---

## Files That Must Not Be Deleted

```text
models/model_metadata.json
models/environment.json
models/requirements-model.txt

outputs/results/model_comparison.csv
outputs/results/cross_validation_results.csv
outputs/results/feature_importance.csv

screenshots/
```

---

## Documentation Requirements

Maintain:

```text
README.md
docs/architecture.md
docs/api.md
docs/model-card.md
docs/demo-guide.md
```

Documentation must use only verified project values.

Do not fabricate:

* Metrics
* Model names
* Feature counts
* Dataset sizes
* Validation scores
* Package versions
* Research citations

Use Mermaid diagrams where useful.

---

## Docker Requirements

The final Docker image should:

* Use a compatible Python version.
* Install exact model dependencies.
* Include only runtime files.
* Exclude raw Kaggle data.
* Exclude notebooks.
* Exclude screenshots.
* Exclude unnecessary outputs.
* Expose one application port.
* Include a health check.
* Run as a non-root user where practical.
* Serve both the FastAPI API and static frontend through one application where possible.

Before declaring success, verify:

```text
Landing page loads
GET /api/health succeeds
GET /api/model/info succeeds
POST /api/predict succeeds
```

---

## Definition of Done

A phase is complete only when:

* The scoped functionality is implemented.
* Required tests exist.
* Tests pass.
* No unrelated files were modified.
* Documentation is updated where necessary.
* Actual commands and results are reported.
* No unsupported claims are made.
* The application remains compatible with the saved model.
* The student can explain the implementation.

---

## Response Format After Each Task

At the end of every Codex task, respond with:

```text
Summary
- What was completed

Files created
- path/to/file

Files modified
- path/to/file

Commands executed
- command

Validation
- tests and actual results

Warnings or unresolved issues
- issue or "None"

Next recommended phase
- one concise recommendation
```

Do not automatically implement the next recommended phase.

