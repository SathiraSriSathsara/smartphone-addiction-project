# SmartHabit model card

## Model overview

SmartHabit uses the saved `LightGBM` binary-classification pipeline in `models/smartphone_addiction_model.joblib`. The model estimates the probability associated with class `1` (`addicted_label`) from 12 raw behavioural and demographic inputs plus four deterministic engineered features. It is an educational university prototype and does not provide a medical or psychological diagnosis.

## Local explanation method

Each successful prediction attempts to generate one local explanation for the same engineered input row. The implementation:

1. applies the fitted pipeline `ColumnTransformer` to the engineered row;
2. obtains the 21 fitted transformed feature names;
3. asks the fitted LightGBM booster for native feature contributions with `pred_contrib=True`;
4. excludes the final expected-value column;
5. groups one-hot contributions back to their raw categorical field and labels that field with the supplied category;
6. ranks grouped contributions by absolute magnitude and returns at most five.

LightGBM documents `pred_contrib=True` as returning feature contributions (SHAP values), with one additional expected-value column. It accepts NumPy and scipy sparse prediction matrices, which makes it compatible with the fitted preprocessing output used by this project. This native path avoids introducing the separately compiled `shap` package solely for basic per-feature contributions. See the official [LightGBM Booster documentation](https://lightgbm.readthedocs.io/en/latest/pythonapi/lightgbm.Booster.html) and [LightGBM C API contribution definition](https://lightgbm.readthedocs.io/en/v4.7.0/C-API.html).

The standalone SHAP `TreeExplainer` also supports LightGBM models, but it is not required by this implementation. See the official [SHAP TreeExplainer documentation](https://shap.readthedocs.io/en/latest/generated/shap.TreeExplainer.html).

## Explanation interpretation

Contribution directions indicate whether a feature pushed the LightGBM raw score toward a higher or lower class-1 estimate for this particular row. They are model influences, not causes.

The API's `display_magnitude` is a relative visual scale. The strongest displayed absolute contribution is assigned `100`, and other displayed factors are scaled against it. These values:

- are not probabilities;
- are not percentage contributions;
- do not add to 100%;
- do not establish causality;
- must not be interpreted as clinical importance.

For categorical inputs, all one-hot columns belonging to the same original field are summed and presented under one readable label such as `Gender: Female`. This prevents inactive encoded categories from being presented as separate user-facing factors.

## Limitations

- Contributions are in the model's raw-score space, not probability space.
- Correlated inputs and engineered ratios can distribute influence in ways that are not intuitive.
- Grouping one-hot columns is a presentation aggregation and can hide opposing encoded contributions within one categorical field.
- The returned list is limited to five factors and is not a complete explanation of the model.
- A direction describes this fitted model's calculation for one row; it does not show that changing the feature will cause a real-world outcome.
- The original LightGBM training version was not recorded. The implementation was verified with LightGBM 4.7.0 under the audited local runtime.
- If preprocessing, contribution generation, feature mapping, or numeric validation fails, the API returns the prediction with an `unavailable` explanation rather than failing the prediction request.

## Responsible use

The probability and explanation should be used only as prompts for reflection about smartphone habits. They must not be used to diagnose addiction, make healthcare decisions, prescribe treatment, or replace a qualified professional.
