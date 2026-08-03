# SmartHabit model card

## Model purpose

SmartHabit uses a saved LightGBM binary-classification pipeline to estimate the probability associated with class `1` of the target `addicted_label`. It accepts a snapshot of behavioural and demographic information and returns an educational risk estimate for reflection.

The system is a CIS6005 Computational Intelligence university project for the Kaggle competition **Predicting Smartphone Addiction — Playground Series Season 6, Episode 8**. It is not a medical device, screening instrument, or psychological assessment.

## Model details

| Item | Verified value |
|---|---|
| Selected estimator | LightGBM classifier inside a saved preprocessing pipeline |
| Artifact | `models/smartphone_addiction_model.joblib` |
| Target | `addicted_label` |
| Classes | 0 and 1 |
| Positive class | 1, probability index 1 |
| Official metric | ROC AUC |
| Random state | 42 |
| Final training rows | 691,369 |
| Saved pipeline inputs | 16 columns |
| Recorded Python | 3.12.13 |
| Recorded pandas | 2.2.2 |
| Recorded NumPy | 2.0.2 |
| Recorded scikit-learn | 1.6.1 |
| Recorded joblib | 1.5.3 |
| Model version | Not recorded |

The original LightGBM training version is not present in `models/environment.json`. The current implementation has been tested locally with LightGBM 4.7.0.

## Data

The model was developed from the data supplied for Kaggle Playground Series Season 6, Episode 8. The final fit recorded in metadata used 691,369 rows. The repository preserves the original train, test, and sample-submission files as training evidence, but the runtime container excludes them.

The Kaggle `id` column is an identifier and is never accepted as a user prediction feature. The target is binary. Repository evidence does not establish that the competition data is clinically collected, clinically validated, or representative of the wider population; no such claim is made.

## Features

### Raw user inputs

Nine numeric fields:

1. `age`
2. `daily_screen_time_hours`
3. `social_media_hours`
4. `gaming_hours`
5. `work_study_hours`
6. `sleep_hours`
7. `notifications_per_day`
8. `app_opens_per_day`
9. `weekend_screen_time`

Three categorical fields:

1. `gender`: Female, Male, Other
2. `stress_level`: High, Low, Medium
3. `academic_work_impact`: No, Yes

All 12 fields are required by the API. Numeric values must be finite and within the observed bounds encoded in `api/schemas.py`.

### Engineered features

The shared inference function creates only the four features used during training:

| Feature | Formula |
|---|---|
| `social_media_ratio` | `social_media_hours / daily_screen_time_hours` |
| `gaming_ratio` | `gaming_hours / daily_screen_time_hours` |
| `notifications_per_screen_hour` | `notifications_per_day / daily_screen_time_hours` |
| `sleep_deficit_from_8h` | `abs(sleep_hours - 8)` |

Zero denominators are replaced with missing values before division, matching the notebook logic, although the API currently requires daily screen time to be at least 0.5 hours.

### Saved preprocessing

The fitted pipeline applies median imputation to numeric columns, most-frequent imputation to categorical columns, and one-hot encoding with unknown categories ignored. The API rejects categories outside the fitted public schema before the pipeline is called.

## Training and validation

The executed notebook uses:

- a stratified 80/20 train-validation split;
- `random_state=42`;
- comparison of Logistic Regression, Random Forest, LightGBM, and MLP Neural Network;
- three-fold stratified cross-validation with shuffling and `random_state=42`; and
- ROC AUC as the official selection metric.

### Verified LightGBM results

| Evaluation | ROC AUC |
|---|---:|
| 20% holdout validation | 0.9597828493169706 |
| Cross-validation fold 1 | 0.9596976806991926 |
| Cross-validation fold 2 | 0.9607739992960643 |
| Cross-validation fold 3 | 0.9606725085892776 |
| Three-fold mean | 0.9603813961948449 |
| Three-fold standard deviation | 0.00048523207515390994 |
| Kaggle public leaderboard | **0.96189** |

The public leaderboard score is a competition ROC AUC result. It is not clinical accuracy, diagnostic accuracy, a treatment outcome, or proof of generalization to real users.

## Prediction output

The application returns class-1 and class-0 probabilities, the highest-probability class, and one display band:

- Low: probability below 0.35
- Moderate: probability from 0.35 to below 0.65
- High: probability 0.65 or above

These thresholds are interface choices. They were not derived as clinical thresholds and must not be presented as such.

## Local explanation method

Each prediction attempts a local explanation for the same input row:

1. the fitted `ColumnTransformer` transforms the engineered row;
2. the implementation retrieves the 21 fitted transformed feature names;
3. the LightGBM booster returns native contribution values with `pred_contrib=True`;
4. the expected-value column is excluded;
5. one-hot columns are grouped back into understandable categorical fields;
6. contributions are ranked by absolute magnitude; and
7. at most five factors are returned.

Directions show whether a feature moved this model's raw score toward a higher or lower class-1 estimate for that row. They are model influences, not causes.

`display_magnitude` scales the strongest displayed absolute contribution to 100 and scales the remaining displayed factors against it. These magnitudes:

- are not probabilities;
- are not percentage causes;
- do not add to 100%;
- do not establish causality; and
- do not measure clinical importance.

If preprocessing, contribution calculation, mapping, or numeric checks fail, the prediction remains available and the explanation returns a safe `unavailable` fallback.

## Intended use

- University teaching and assessment demonstration.
- Exploration of an end-to-end competition machine-learning workflow.
- Personal reflection on supplied smartphone-use patterns.
- Demonstration of validated APIs, local model explanation, and responsible result presentation.

## Prohibited use

- Diagnosing smartphone addiction or any medical or psychological condition.
- Replacing a healthcare or mental-health professional.
- Recommending treatment, medication, or clinical intervention.
- Making decisions about employment, education, insurance, credit, access to services, or legal matters.
- Labelling an individual as medically addicted.
- Presenting probabilities, risk bands, or explanation factors as clinical certainty or causes.
- Monitoring or profiling people without their knowledge and appropriate authority.

## Ethical risks

- **Representation bias:** competition data may not represent all ages, regions, cultures, socioeconomic groups, devices, or patterns of use.
- **Self-report bias:** users may estimate time and notifications inaccurately or interpret categories differently.
- **Automation bias:** a numerical probability can appear more authoritative than the evidence supports.
- **Stigma:** labels related to addiction may affect self-perception or how others treat a user.
- **Privacy:** behavioural, stress, sleep, and impact fields can be sensitive even without a name.
- **Explanation misuse:** model contributions can be mistaken for causes or advice.

Mitigations include data minimisation, no `id` field, strict validation, no application database or accounts, non-diagnostic wording, explicit uncertainty, display-threshold labels, explanation limitations, and a dedicated disclaimer page.

## Limitations

- The repository provides competition evaluation, not prospective real-world or clinical validation.
- Model performance may change under distribution shift.
- Inputs omit contextual factors that may matter to a person's wellbeing.
- Correlated raw and ratio features can distribute explanation influence in unintuitive ways.
- Grouping one-hot contributions improves readability but can hide opposing encoded effects.
- Only five factors are displayed, so explanations are incomplete.
- The model version is absent from saved metadata.
- The training LightGBM version is absent from the recorded environment.
- The current public application has no application-level rate limiter; deployment infrastructure should supply one for broad public exposure.

## Monitoring and maintenance

The application validates required artifacts and pickle-critical dependencies at startup and logs runtime compatibility warnings. Any future model replacement should repeat the repository audit, update metadata and schema together, rerun the complete tests, and re-evaluate data representativeness and model performance. The existing saved model must not be silently replaced or retrained.
