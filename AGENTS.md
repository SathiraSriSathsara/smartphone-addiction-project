# Smartphone Addiction Prediction Project

## Project objective

Develop a complete machine-learning solution for the Kaggle competition:

Predicting Smartphone Addiction
Playground Series - Season 6 Episode 8

The project must include:

1. Dataset inspection
2. Exploratory data analysis
3. Reproducible preprocessing
4. Multiple baseline and advanced models
5. Cross-validation
6. Official Kaggle metric evaluation
7. Hyperparameter tuning
8. Kaggle submission generation
9. Saved production model
10. FastAPI prediction service
11. Web frontend
12. Automated tests
13. Technical documentation

## Critical rules

- Never invent dataset columns.
- Inspect the actual CSV files before implementing models.
- Read the target from train.csv versus test.csv.
- Use sample_submission.csv as the submission template.
- Do not fabricate scores or results.
- Do not claim that code ran unless it ran successfully.
- Keep all experiments reproducible using random_state=42.
- Prevent preprocessing leakage.
- Fit preprocessing only on training folds.
- Use the official Kaggle evaluation metric.
- Preserve all experiment results in outputs/results.
- Do not overwrite previous submissions.
- Name submissions submission_v01.csv, submission_v02.csv, etc.
- Add type hints and error handling to production Python files.
- Use pipelines so the API applies exactly the same preprocessing as training.
- Add tests before considering a phase complete.
- Do not modify files outside this repository.

## Academic integrity

- Generated material is a development aid, not automatically final coursework.
- Add comments explaining important decisions.
- Record all external notebooks, papers and code references.
- Do not copy Kaggle solutions without attribution.
- Do not generate fake citations, screenshots or experimental results.
- The student must be able to explain every model and code path.

## Workflow

Work one phase at a time.

For each phase:

1. Inspect existing files.
2. Propose a plan.
3. Implement the phase.
4. Run tests or notebooks.
5. Report files changed.
6. Report commands executed.
7. Report actual results.
8. Stop and request review before proceeding to the next major phase.