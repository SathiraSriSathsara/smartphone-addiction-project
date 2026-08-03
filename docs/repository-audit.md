# Repository and model audit

Audit date: 2026-08-03

## Scope and safeguards

This was a read-only audit of the repository and protected evidence files. The only created artifacts are this report and `docs/model-schema.json`. The notebook, datasets, saved model, metadata, results, submissions, and screenshots were not modified.

The repository contains the expected top-level directories `api`, `data`, `models`, `notebooks`, `outputs`, `screenshots`, `src`, `tests`, and `web`. At audit time, the tracked implementation consisted primarily of the notebook, model artifacts, and generated results/figures; `README.md` and the root `requirements.txt` were empty, and no files were present under `api`, `src`, `tests`, or `web`.

## Recorded model environment

`models/environment.json` and `models/requirements-model.txt` record:

| Component | Recorded version |
|---|---:|
| Python | 3.12.13 |
| pandas | 2.2.2 |
| NumPy | 2.0.2 |
| scikit-learn | 1.6.1 |
| joblib | 1.5.3 |
| LightGBM | Not pinned or recorded |

The available runtime initially used Python 3.13.14, pandas 2.2.3, NumPy 2.2.3, scikit-learn 1.9.0, and joblib 1.5.3, with LightGBM absent. An isolated exact installation was attempted, but pandas 2.2.2 had no compatible wheel for Python 3.13 and its source metadata/build step failed. Loading under scikit-learn 1.9.0 then failed because the pickle references the 1.6.1 private class `_RemainderColsList`.

The trusted model loaded successfully, without warnings, after using scikit-learn 1.6.1 and joblib 1.5.3. The successful inspection runtime was Python 3.13.14, pandas 2.2.3, NumPy 2.2.3, scikit-learn 1.6.1, joblib 1.5.3, and LightGBM 4.7.0. This validates the model structure but is not an exact reproduction of the training runtime because Python, pandas, NumPy, and the unknown original LightGBM version could not be matched.

## Saved model structure

The serialized object is an `sklearn.pipeline.Pipeline` with these steps:

1. `preprocessor`: `sklearn.compose.ColumnTransformer`
2. `model`: `lightgbm.sklearn.LGBMClassifier`

The numeric transformer selects 13 fields and applies `SimpleImputer(strategy="median")`. It does not scale values. The categorical transformer selects three fields and applies `SimpleImputer(strategy="most_frequent")`, followed by `OneHotEncoder(handle_unknown="ignore")`.

The fitted categorical values are:

| Field | Learned categories |
|---|---|
| `gender` | `Female`, `Male`, `Other` |
| `stress_level` | `High`, `Low`, `Medium` |
| `academic_work_impact` | `No`, `Yes` |

The pipeline and estimator both expose `predict_proba`. Their class order is exactly `[0, 1]`, so the addiction probability for positive class `1` is column/index 1. A smoke prediction using the fitted imputer statistics returned probabilities `[0.31249272255304716, 0.6875072774469528]`, which are within `[0, 1]` and sum to 1.0. This smoke result verifies runtime behaviour only; it is not a performance metric or a clinically meaningful example.

## Exact feature contract

The model's `feature_names_in_` contains 16 post-engineering fields in this exact order:

1. `age`
2. `daily_screen_time_hours`
3. `social_media_hours`
4. `gaming_hours`
5. `work_study_hours`
6. `sleep_hours`
7. `notifications_per_day`
8. `app_opens_per_day`
9. `weekend_screen_time`
10. `gender`
11. `stress_level`
12. `academic_work_impact`
13. `social_media_ratio`
14. `gaming_ratio`
15. `notifications_per_screen_hour`
16. `sleep_deficit_from_8h`

The first 12 are raw user/model-domain fields. The last four are engineered fields and must be created before invoking the saved pipeline:

- `social_media_ratio = social_media_hours / daily_screen_time_hours`
- `gaming_ratio = gaming_hours / daily_screen_time_hours`
- `notifications_per_screen_hour = notifications_per_day / daily_screen_time_hours`
- `sleep_deficit_from_8h = abs(sleep_hours - 8)`

For each ratio, notebook cell 23 replaces a zero `daily_screen_time_hours` denominator with a missing value before division. The pipeline then median-imputes the resulting numeric missing value.

All numeric source columns are stored as `float64` in the training and test datasets because missing values are present, including age and count-like fields. The portable request type is therefore `number`; integer-only semantics are not established by the saved metadata. `id` is excluded and must never be supplied as a prediction feature.

The authoritative machine-readable contract is in `docs/model-schema.json`. It marks all 12 raw fields required for a future request object and all four engineered fields as backend-derived rather than user-supplied. Although the fitted pipeline can impute missing values, the repository does not define an API nullability policy, numeric bounds, or a distinction between an omitted required key and a present null value.

## Metadata and notebook comparison

The metadata's 16 `feature_columns`, 13 `numeric_columns`, three `categorical_columns`, and four `engineered_features` match the loaded pipeline exactly, including order. The target is `addicted_label`, the excluded identifier is `id`, and the estimator is the expected LightGBM classifier.

Notebook cell 23 defines the four reported engineered features with formulas matching the metadata and pipeline inputs. Notebook cells 27 and 29 define preprocessing and the LightGBM pipeline matching the loaded object: numeric median imputation, categorical most-frequent imputation, unknown-safe one-hot encoding, and an `LGBMClassifier`. Notebook cell 42 saves the pipeline and produces the inspected metadata files.

One important deployment boundary is confirmed: feature engineering is **not** a step inside the saved sklearn pipeline. The application must call the shared equivalent of notebook `add_domain_features` before passing the 16-column frame to `predict_proba`. Passing only the 12 raw fields directly to the saved pipeline will fail its feature contract.

## Findings and unresolved issues

1. The exact LightGBM training version is absent from both `environment.json` and `requirements-model.txt`; the latter contains only unpinned `lightgbm`. Full environment reproduction is therefore impossible from repository evidence.
2. The current machine has no Python 3.12 interpreter exposed through the Python launcher, and pandas 2.2.2 could not be installed under Python 3.13. The exact recorded environment was not reproduced.
3. The pickle is incompatible with scikit-learn 1.9.0 because it depends on the private 1.6.1 `_RemainderColsList` symbol. Model-runtime scikit-learn must remain pinned to 1.6.1 unless the model is deliberately re-exported and retested.
4. Metadata does not record model/application version, LightGBM version, numeric validation ranges, request nullability, or explicit categorical values. Categories were recoverable from the fitted encoder; safe numeric bounds require a separate, evidence-based API design decision.
5. The saved pipeline does not contain feature engineering. Inference code must reproduce notebook cell 23 exactly and preserve input immutability.
6. No mismatch was found between the notebook's final feature engineering/preprocessing definitions, `model_metadata.json`, and the loaded saved pipeline.

## Audit conclusion

The saved artifact is a functional binary LightGBM classification pipeline when loaded with scikit-learn 1.6.1. It expects 16 post-engineering columns, supports probability prediction, and uses class `1` as the positive class at probability index 1. The schema is sufficiently discoverable for a later API phase, subject to resolving validation bounds/nullability and pinning the original LightGBM version if it can be recovered from the training environment.
