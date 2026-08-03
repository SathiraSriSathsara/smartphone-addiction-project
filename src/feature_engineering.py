"""Feature engineering shared by training-compatible inference code."""

import numpy as np
import pandas as pd


def add_domain_features(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with the domain features used to train the saved model.

    A feature is added only when all of its source columns are present. Ratio
    denominators equal to zero are replaced with missing values before division,
    matching the training notebook so the saved pipeline can impute them.

    Args:
        dataframe: Raw input features. The caller's DataFrame is not modified.

    Returns:
        A new DataFrame containing the original columns in their original order,
        followed by every derivable engineered feature in training order.
    """
    result = dataframe.copy()

    candidate_pairs = [
        (
            "social_media_ratio",
            "social_media_hours",
            "daily_screen_time_hours",
        ),
        (
            "gaming_ratio",
            "gaming_hours",
            "daily_screen_time_hours",
        ),
        (
            "notifications_per_screen_hour",
            "notifications_per_day",
            "daily_screen_time_hours",
        ),
    ]

    for new_column, numerator, denominator in candidate_pairs:
        if {numerator, denominator}.issubset(result.columns):
            safe_denominator = result[denominator].replace(0, np.nan)
            result[new_column] = result[numerator] / safe_denominator

    if "sleep_hours" in result.columns:
        result["sleep_deficit_from_8h"] = (result["sleep_hours"] - 8).abs()

    return result
