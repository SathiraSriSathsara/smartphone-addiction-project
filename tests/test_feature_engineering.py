"""Tests for training-compatible domain feature engineering."""

import numpy as np
import pandas as pd
import pandas.testing as pdt

from src.feature_engineering import add_domain_features


def test_add_domain_features_with_valid_input() -> None:
    """All four trained features have the notebook's expected values."""
    dataframe = pd.DataFrame(
        {
            "daily_screen_time_hours": [10.0, 4.0],
            "social_media_hours": [2.5, 1.0],
            "gaming_hours": [3.0, 0.5],
            "notifications_per_day": [50.0, 12.0],
            "sleep_hours": [6.5, 9.0],
        }
    )

    result = add_domain_features(dataframe)

    pdt.assert_series_equal(
        result["social_media_ratio"],
        pd.Series([0.25, 0.25], name="social_media_ratio"),
    )
    pdt.assert_series_equal(
        result["gaming_ratio"],
        pd.Series([0.3, 0.125], name="gaming_ratio"),
    )
    pdt.assert_series_equal(
        result["notifications_per_screen_hour"],
        pd.Series([5.0, 3.0], name="notifications_per_screen_hour"),
    )
    pdt.assert_series_equal(
        result["sleep_deficit_from_8h"],
        pd.Series([1.5, 1.0], name="sleep_deficit_from_8h"),
    )


def test_zero_denominators_produce_missing_ratios() -> None:
    """Zero screen time produces NaN rather than infinite ratio values."""
    dataframe = pd.DataFrame(
        {
            "daily_screen_time_hours": [0.0],
            "social_media_hours": [2.0],
            "gaming_hours": [1.0],
            "notifications_per_day": [20.0],
        }
    )

    result = add_domain_features(dataframe)

    ratio_columns = [
        "social_media_ratio",
        "gaming_ratio",
        "notifications_per_screen_hour",
    ]
    assert result[ratio_columns].isna().all().all()
    assert not np.isinf(result[ratio_columns].to_numpy()).any()


def test_missing_optional_source_columns_skip_only_affected_features() -> None:
    """Features without complete source pairs are not created."""
    dataframe = pd.DataFrame(
        {
            "daily_screen_time_hours": [5.0],
            "social_media_hours": [2.0],
            "sleep_hours": [7.0],
        }
    )

    result = add_domain_features(dataframe)

    assert "social_media_ratio" in result.columns
    assert "sleep_deficit_from_8h" in result.columns
    assert "gaming_ratio" not in result.columns
    assert "notifications_per_screen_hour" not in result.columns


def test_input_dataframe_is_not_mutated() -> None:
    """Feature engineering returns an independent DataFrame copy."""
    dataframe = pd.DataFrame(
        {
            "daily_screen_time_hours": [4.0],
            "social_media_hours": [1.0],
        }
    )
    original = dataframe.copy(deep=True)

    result = add_domain_features(dataframe)
    result.loc[0, "daily_screen_time_hours"] = 99.0

    pdt.assert_frame_equal(dataframe, original)
    assert result is not dataframe


def test_output_column_order_matches_training_order() -> None:
    """Original order is preserved and derived columns are appended in order."""
    dataframe = pd.DataFrame(
        {
            "age": [21.0],
            "daily_screen_time_hours": [8.0],
            "social_media_hours": [2.0],
            "gaming_hours": [1.0],
            "notifications_per_day": [24.0],
            "sleep_hours": [7.0],
            "gender": ["Female"],
        }
    )

    result = add_domain_features(dataframe)

    assert result.columns.tolist() == [
        *dataframe.columns,
        "social_media_ratio",
        "gaming_ratio",
        "notifications_per_screen_hour",
        "sleep_deficit_from_8h",
    ]
