# Final report evidence inventory

Audit date: 4 August 2026  
Project: Predicting Smartphone Addiction Using Computational Intelligence  
Module and assessment: CIS6005 Computational Intelligence, WRIT1  
Student ID: 20302367

## 1. Audit status and evidence gate

This inventory was created before academic-source research or report drafting, as required by the supplied report instruction. The complete repository, executed notebook, raw CSV files, saved model, application, tests, generated outputs, and 11-page assessment brief were inspected read-only.

**Evidence-gate decision: STOP BEFORE REPORT DRAFTING.** Core assessment evidence is missing:

1. **Final/private Kaggle submission evidence: NOT VERIFIED.** The assessment brief explicitly requires at least one public and one final/private leaderboard submission. No submission-history screenshot, selected-final-submission screenshot, private leaderboard score, or other final-selection evidence is present.
2. **Public leaderboard evidence: NOT VERIFIED IN THE REPOSITORY.** The value `0.96189` is stated as verified in `AGENTS.md` and the supplied task instruction, but `screenshots/` is empty and there is no Kaggle export or response file independently linking that score to this submission.
3. **Competition eligibility dates: NOT VERIFIED.** The brief requires an active competition or one concluded within two months before the 2026 submission deadline, with defined start/end dates. No repository artifact records the competition dates or Moodle deadline.
4. **Practical-demonstration screenshots: NOT VERIFIED.** The application and API execute successfully, but `screenshots/` contains no landing, form, result, Swagger, health, test, or model-info evidence.

Report drafting, literature research, citations, DOCX, and final PDF generation were therefore not started in this phase.

## 2. Assessment-brief evidence

Source: `mnt/data/ICBT_CIS6005_S1SRI_WRIT1_Nov-2026_Main_2025-26.pdf`  
Pages: 11  
SHA-256: `740FA7C0F73D6121670B9BE243A011E3A2ACE8B9DF92E856C4609137D48187DB`

The full brief was text-extracted and every page was rendered for visual inspection. Verified requirements include:

- assessment title: Deep learning Plus AI Mini project;
- assessment ID: WRIT1;
- weighting: 100%;
- maximum report length: 4,000 words;
- word count normally includes text, tables, calculations, figures, subtitles, and citations;
- reference lists and appendix contents are excluded;
- Harvard referencing is required unless stated otherwise;
- submission format is PDF through the Moodle/Turnitin point;
- filename/title must contain student ID, module code, and assessment ID;
- one public and one final/private Kaggle submission are required;
- a working desktop, web, mobile, or API application using the trained model is required;
- the selected competition must be active or have concluded within two months before the 2026 deadline and must have defined start/end dates;
- submission time is 2:00 p.m. on the Moodle deadline day; the actual deadline is not printed and is to be provided on Moodle.

### Assessed areas stated in the task list

| Criterion | Marks |
|---|---:|
| Comprehensive overview of Computational Intelligence and comparison with traditional AI | 10 |
| Critical literature review of research and similar applications | 20 |
| Exploratory data analysis and influence on model design | 10 |
| System architecture, differentiation, and ML techniques | 10 |
| Full model evaluation, implementation details, and practical demonstration | 40 |
| Critical evaluation and suitability of deep learning, limitations, research, and emerging improvements | 10 |

### Rubric inconsistency requiring cautious handling

The detailed rubric on pages 7-9 lists the first five areas above, but labels the final 10-mark row **Conclusion**, whereas the task list on page 3 assigns those 10 marks to critical model/deep-learning evaluation. This is an internal brief inconsistency. A future report should visibly address both critical evaluation/deep-learning suitability and a concise conclusion, without claiming how the marker will resolve the discrepancy.

The excellent band emphasizes analytical comparison, correct citations, extensive EDA insight, clear explanation of why techniques work, and the ability to navigate code flow, function calls, inputs, outputs, and libraries during the practical demonstration.

## 3. Integrity hashes for primary evidence

| Artifact | SHA-256 |
|---|---|
| Saved model | `AF59E03DC5F151FF60B1E6B167BC1602EFB7CD1858EE9A43DEFE4B545DC40DFA` |
| Executed notebook | `0FD9AF56CB1FB2FF08A4D3BFDC1D340E622F90AA2150CD89264AE4AE12882378` |
| LightGBM submission CSV | `7CDDC449F4B70B7F5EA3127E070130EB76C26AF730577102AA413DABBED81AAE` |

## 4. Dataset evidence

Sources: `data/train.csv`, `data/test.csv`, `data/sample_submission.csv`, `outputs/results/dataset_summary.json`, and executed notebook cells.

### Dimensions and columns

| Dataset | Rows | Columns | Verified role |
|---|---:|---:|---|
| Training | 691,369 | 14 | ID, 12 raw features, and target |
| Test | 296,302 | 13 | ID and 12 raw features |
| Generated submission | 296,302 | 2 | ID and predicted target probability |

- Target variable: `addicted_label`.
- ID column: `id`.
- The ID is excluded from model input.
- Raw numerical features: `age`, `daily_screen_time_hours`, `social_media_hours`, `gaming_hours`, `work_study_hours`, `sleep_hours`, `notifications_per_day`, `app_opens_per_day`, and `weekend_screen_time`.
- Raw categorical features: `gender`, `stress_level`, and `academic_work_impact`.

### Missing values

Total missing training cells: 870,360.  
Training rows containing at least one missing value: 422,184.

| Field | Missing | Percentage |
|---|---:|---:|
| `social_media_hours` | 133,995 | 19.381112% |
| `gaming_hours` | 126,821 | 18.343461% |
| `weekend_screen_time` | 112,063 | 16.208855% |
| `daily_screen_time_hours` | 95,854 | 13.864376% |
| `app_opens_per_day` | 80,710 | 11.673940% |
| `notifications_per_day` | 67,584 | 9.775388% |
| `stress_level` | 55,148 | 7.976638% |
| `work_study_hours` | 51,518 | 7.451592% |
| `sleep_hours` | 44,480 | 6.433612% |
| `academic_work_impact` | 44,224 | 6.396584% |
| `gender` | 29,034 | 4.199494% |
| `age` | 28,929 | 4.184307% |
| `id` | 0 | 0% |
| `addicted_label` | 0 | 0% |

### Duplicate findings

- Exact duplicate training rows: 0.
- Duplicate training IDs: 0.
- Duplicate generated-submission IDs: 0.

### Target distribution

| Class | Count | Percentage |
|---|---:|---:|
| 0 | 200,895 | 29.057565% |
| 1 | 490,474 | 70.942435% |

The target is imbalanced toward class 1. Notebook cell 25 verifies that stratification retained approximately 70.9424% class 1 and 29.0576% class 0 in both the training and validation partitions.

### Categorical distribution

| Feature | Observed non-missing counts |
|---|---|
| `gender` | Male 223,662; Female 221,595; Other 217,078 |
| `stress_level` | High 220,873; Low 207,783; Medium 207,565 |
| `academic_work_impact` | Yes 330,566; No 316,579 |

### Train/test comparison

`outputs/results/train_test_numeric_comparison.csv` compares means and standard deviations for all nine numeric inputs. Absolute standardized mean differences range from approximately `0.000035` to `0.002226`, providing repository evidence that these aggregate numeric moments are closely aligned. This does not prove identical distributions or absence of distribution shift.

## 5. EDA evidence and available figures

There are 22 PNG figures in `outputs/figures/`. All were opened in a contact sheet and were legible at source resolution.

### Core report candidates

- `target_distribution.png`: class-count bar chart.
- `correlation_matrix.png`: numerical feature correlation heatmap including target.
- `daily_screen_time_hours_by_target.png`: strong class-separated boxplot.
- `social_media_hours_by_target.png`: class-separated boxplot.
- `weekend_screen_time_by_target.png`: class-separated boxplot.
- `best_model_confusion_matrix.png`: LightGBM confusion matrix.
- `feature_importance.png`: LightGBM split importance.

The confusion-matrix figure visibly records: true 0/predicted 0 = 32,330; true 0/predicted 1 = 7,849; true 1/predicted 0 = 6,523; true 1/predicted 1 = 91,572. These values sum to the 138,274-row validation set.

### Additional figures

- Nine numeric distribution charts: age, daily screen time, social media, gaming, work/study, sleep, notifications, app opens, and weekend screen time.
- Nine feature-by-target boxplots for the same numerical inputs.

### EDA-to-design evidence present in the notebook

| EDA evidence | Implemented model-design response |
|---|---|
| Target imbalance | Stratified split/CV; accuracy supplemented by balanced accuracy, F1, ROC AUC, precision, recall, and log loss |
| Numeric missing values | Median imputation inside each pipeline |
| Categorical missing values | Most-frequent imputation inside each pipeline |
| Different numeric scales | StandardScaler for Logistic Regression and MLP only |
| Categorical features | One-hot encoding with unknown categories ignored |
| Nonlinear feature-target separation visible in plots | Comparison of Random Forest and LightGBM against linear and MLP baselines |

Notebook cell 21 is explicitly labelled an “EDA interpretation template.” Its generic wording must not be copied as a completed finding without tying each decision to the generated outputs above.

## 6. Feature engineering and preprocessing

Notebook cell 23 and `src/feature_engineering.py` verify four added fields, increasing model input from 12 raw columns to 16:

| Engineered feature | Formula |
|---|---|
| `social_media_ratio` | `social_media_hours / daily_screen_time_hours` |
| `gaming_ratio` | `gaming_hours / daily_screen_time_hours` |
| `notifications_per_screen_hour` | `notifications_per_day / daily_screen_time_hours` |
| `sleep_deficit_from_8h` | `abs(sleep_hours - 8)` |

Ratio denominators equal to zero are replaced with missing values before division. The shared inference function returns a copy and preserves training order.

Preprocessing is fitted only inside scikit-learn pipelines:

- Logistic Regression and MLP: median numeric imputation, standard scaling, most-frequent categorical imputation, and one-hot encoding.
- Random Forest and LightGBM: median numeric imputation without scaling, most-frequent categorical imputation, and one-hot encoding.
- `OneHotEncoder(handle_unknown="ignore", sparse_output=True)` is used.

## 7. Models, validation, and final selection

### Validation strategy

- Holdout: stratified 80/20 split.
- Training partition: 553,095 rows and 16 features.
- Validation partition: 138,274 rows and 16 features.
- Split seed: `random_state=42`.
- Cross-validation: three-fold `StratifiedKFold`, shuffle enabled, `random_state=42`.
- Cross-validation was run for the top two holdout models: LightGBM and Random Forest.
- Notebook-configured official metric: ROC AUC.

The notebook itself contains a warning to confirm the official Kaggle metric. `AGENTS.md` states ROC AUC is verified, but no captured Kaggle Evaluation page is present. Independent Kaggle metric-page evidence is therefore **NOT VERIFIED** in the repository.

### Holdout model comparison

| Model | Accuracy | Balanced accuracy | Precision | Recall | F1 | ROC AUC | Log loss | Training seconds |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| LightGBM | 0.896061 | 0.869076 | 0.921053 | 0.933503 | 0.927236 | 0.959783 | 0.232504 | 47.059773 |
| Random Forest | 0.847310 | 0.857831 | 0.945560 | 0.832713 | 0.885556 | 0.939089 | 0.300440 | 350.184982 |
| MLP Neural Network | 0.863554 | 0.819237 | 0.887400 | 0.925042 | 0.905830 | 0.937364 | 0.283152 | 104.613218 |
| Logistic Regression | 0.833389 | 0.835477 | 0.927057 | 0.830491 | 0.876122 | 0.914720 | 0.381927 | 303.959277 |

### Cross-validation

| Model | Fold 1 | Fold 2 | Fold 3 | Mean | Standard deviation |
|---|---:|---:|---:|---:|---:|
| LightGBM | 0.959698 | 0.960774 | 0.960673 | 0.960381 | 0.000485 |
| Random Forest | 0.939074 | 0.940262 | 0.940061 | 0.939799 | 0.000519 |

### Final model

- Selected model: LightGBM.
- Final fit: all 691,369 training rows and 16 columns.
- Recorded final-fit time: 62.746633274 seconds.
- Saved object: `sklearn.pipeline.Pipeline` with `ColumnTransformer` and `lightgbm.sklearn.LGBMClassifier`.
- Loaded classes: `[0, 1]`.
- `predict` and `predict_proba`: supported.
- Transformed features: 21.
- Loaded `feature_names_in_` exactly matches metadata order.

Verified final LightGBM parameters include: 600 estimators; learning rate 0.04; 31 leaves; max depth -1; minimum child samples 30; subsample 0.85; column sample 0.85; L1 regularisation 0.1; L2 regularisation 0.2; binary objective; and random state 42.

## 8. Kaggle submission evidence

`outputs/submissions/submission_lightgbm.csv` is present and internally valid:

- rows: 296,302;
- columns: `id`, `addicted_label`;
- IDs exactly match `data/test.csv` in order;
- missing values: 0;
- duplicate IDs: 0;
- minimum prediction: 0.0007128251615279;
- maximum prediction: 0.9999929514022292;
- mean prediction: 0.709304009965153.

### Leaderboard evidence status

| Evidence | Status |
|---|---|
| Valid local submission file | VERIFIED |
| Public score `0.96189` stated in project instructions | VERIFIED AS PROVIDED CLAIM; repository screenshot/export absent |
| Public leaderboard screenshot | NOT VERIFIED |
| Public rank 360 | NOT VERIFIED |
| Submission-history screenshot | NOT VERIFIED |
| Selected final/private submission | NOT VERIFIED |
| Private/final leaderboard score | NOT VERIFIED |
| Competition start/end dates and eligibility window | NOT VERIFIED |

No private score or rank may be inserted in the report unless the student supplies direct evidence.

## 9. Application architecture and functionality

### Runtime architecture

`web/` static frontend -> FastAPI -> Pydantic validation -> one-row pandas DataFrame -> shared `add_domain_features` -> saved preprocessing pipeline -> LightGBM `predict_proba` -> application risk band and local factors -> frontend dashboard.

FastAPI loads the trusted model once during lifespan startup. `ModelService` validates required files, reads metadata/environment/schema, checks package compatibility, deserializes the local model, confirms methods and exact feature order, and stores the singleton on application state.

### Implemented JSON API endpoints

| Method | Endpoint | Verified purpose |
|---|---|---|
| GET | `/api/health` | Status, environment, application version, timestamp |
| GET | `/api/model/info` | Allow-listed model metadata |
| GET | `/api/model/schema` | Twelve raw frontend fields and categories |
| POST | `/api/predict` | Validated probability, class, risk band, disclaimer, local factors/fallback |

FastAPI also serves the frontend at `/`, Swagger at `/docs`, ReDoc at `/redoc`, and OpenAPI JSON at `/openapi.json`.

### Frontend functionality

Verified pages:

- `index.html`: responsive landing page and prediction CTA;
- `predict.html`: schema-driven 12-field form, browser validation, loading/reset state, safe server errors, probability gauge, result details, three risk cards, local explanation, start-new-assessment action, and print styles;
- `about.html`: project and competition context;
- `model.html`: model workflow, verified evaluation results, and limitations;
- `disclaimer.html`: educational use, privacy, limitations, and professional/emergency support wording.

The frontend is plain HTML, CSS, and JavaScript. It has skip links, semantic regions, dynamic labels/descriptions, inline errors, keyboard focus styling, responsive breakpoints, accessible contrast, and reduced-motion handling.

### Security and reliability controls

- Strict Pydantic bounds, finite-number checks, categories, required fields, and extra-field rejection.
- Explicit environment-configured CORS origins; wildcard origins rejected.
- 16,384-byte default body limit.
- UUID request ID on responses/logs.
- Structured logs excluding request bodies and query strings.
- Sanitized error envelopes without stack traces, rejected values, package internals, or local paths.
- Security headers and production HSTS.
- Non-root, one-port Docker configuration is present, but an actual Docker build remains **NOT VERIFIED** because Docker was unavailable during the preceding container phase.

## 10. Automated test evidence

Command executed during this audit: `pytest -q`.

Result: **39 passed in 1.77 seconds**.

The suite covers:

- feature engineering, zero denominators, missing optional source fields, input immutability, and output order;
- required model artifacts, compatibility checks, singleton loading, schema/info methods, and missing-file behavior;
- root/static serving and health;
- valid predictions, real saved-model integration, probability bounds, risk mapping, response keys, and safe unexpected errors;
- missing fields, invalid categories, impossible numeric ranges, non-finite values, and extra fields;
- local explanation response structure, aggregation, factor limit, directions, normalization, and fallback;
- request IDs, response headers, request-size rejection, validation-value redaction, and unsafe CORS rejection.

`python -m compileall -q api src` also completed without syntax errors.

## 11. Software-version evidence

### Recorded training environment

| Software | Recorded version |
|---|---|
| Python | 3.12.13 |
| pandas | 2.2.2 |
| NumPy | 2.0.2 |
| scikit-learn | 1.6.1 |
| joblib | 1.5.3 |
| LightGBM | NOT VERIFIED - omitted from `environment.json` and unpinned in `requirements-model.txt` |

### Application dependency pins

| Software | `requirements.txt` version |
|---|---|
| FastAPI | 0.115.9 |
| HTTPX | 0.28.1 |
| NumPy | 2.0.2 |
| pandas | 2.2.2 |
| pydantic-settings | 2.9.1 |
| pytest | 9.1.1 |
| Uvicorn | 0.34.2 |
| joblib | 1.5.3 |
| scikit-learn | 1.6.1 |
| LightGBM | 4.7.0 |

Local audit runtime differences were Python 3.13.14, pandas 2.2.3, and NumPy 2.2.3. scikit-learn 1.6.1 and joblib 1.5.3 matched the recorded pickle-critical versions. These local differences generated warnings; they are not the recorded training environment.

## 12. Screenshot and demonstration evidence

`screenshots/` exists but contains zero files.

The following are all **NOT VERIFIED** as screenshot evidence:

- landing page;
- completed prediction form;
- Low, Moderate, and High results;
- validation error;
- local explanation factors;
- Swagger documentation;
- API health response;
- model information response;
- passing test output;
- Kaggle submission history;
- public leaderboard score/rank;
- selected final/private submission;
- private leaderboard result;
- container health and image size.

The running application was verified programmatically, but programmatic success is not a substitute for the practical-demonstration and Kaggle screenshots requested by the report instruction.

## 13. Academic-source and citation evidence

Academic-source research has not yet been performed because Phase 1 found blocking evidence gaps. Therefore:

- peer-reviewed literature set: NOT VERIFIED;
- Harvard in-text citations: NOT CREATED;
- Harvard reference list: NOT CREATED;
- DOI/reference checks: NOT PERFORMED;
- application-comparison evidence from external sources: NOT VERIFIED.

No research paper, citation, DOI, or external performance claim has been invented.

## 14. Core unresolved evidence required from the student

Before Phase 2 research or report drafting, obtain and place verified evidence in `screenshots/` (or another clearly documented evidence location):

1. Kaggle competition Overview page showing competition identity and start/end dates.
2. Kaggle Evaluation page showing the official metric.
3. Submission history showing at least one public submission.
4. Evidence that a final/private submission was selected, as required by the brief.
5. Private/final leaderboard result, if released; otherwise a screenshot showing its current unreleased/not-available status.
6. Public leaderboard screenshot clearly linking the project/submission to score `0.96189` and any rank intended for the report.
7. Practical application screenshots listed in `docs/demo-guide.md`.
8. Moodle submission deadline and any current AI-use disclosure policy applicable to this assessment.

Until those are supplied, the final report must not claim compliance with the public-plus-final/private submission requirement, a public rank, a private score, competition-date eligibility, or completed screenshot evidence.
