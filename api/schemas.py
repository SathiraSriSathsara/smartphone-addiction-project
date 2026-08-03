"""Validated request and response contracts for prediction endpoints."""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

FiniteAge = Annotated[
    float,
    Field(ge=18.0, le=35.0, allow_inf_nan=False, strict=True),
]
DailyScreenTime = Annotated[
    float,
    Field(ge=0.5, le=15.0, allow_inf_nan=False, strict=True),
]
SocialMediaHours = Annotated[
    float,
    Field(ge=0.0, le=8.0, allow_inf_nan=False, strict=True),
]
GamingHours = Annotated[
    float,
    Field(ge=0.0, le=4.0, allow_inf_nan=False, strict=True),
]
WorkStudyHours = Annotated[
    float,
    Field(ge=0.0, le=6.0, allow_inf_nan=False, strict=True),
]
SleepHours = Annotated[
    float,
    Field(ge=4.5, le=9.0, allow_inf_nan=False, strict=True),
]
NotificationsPerDay = Annotated[
    float,
    Field(ge=20.0, le=250.0, allow_inf_nan=False, strict=True),
]
AppOpensPerDay = Annotated[
    float,
    Field(ge=15.0, le=180.0, allow_inf_nan=False, strict=True),
]
WeekendScreenTime = Annotated[
    float,
    Field(ge=0.51, le=17.56, allow_inf_nan=False, strict=True),
]
Probability = Annotated[float, Field(ge=0.0, le=1.0, allow_inf_nan=False)]


class PredictionRequest(BaseModel):
    """The exact 12 raw features supplied before feature engineering."""

    model_config = ConfigDict(extra="forbid")

    age: FiniteAge
    daily_screen_time_hours: DailyScreenTime
    social_media_hours: SocialMediaHours
    gaming_hours: GamingHours
    work_study_hours: WorkStudyHours
    sleep_hours: SleepHours
    notifications_per_day: NotificationsPerDay
    app_opens_per_day: AppOpensPerDay
    weekend_screen_time: WeekendScreenTime
    gender: Literal["Female", "Male", "Other"]
    stress_level: Literal["High", "Low", "Medium"]
    academic_work_impact: Literal["No", "Yes"]


class PredictionResponse(BaseModel):
    """Educational model prediction returned to API clients."""

    predicted_class: int
    addiction_probability: Probability
    non_addiction_probability: Probability
    risk_level: Literal["Low", "Moderate", "High"]
    risk_message: str
    model_version: str | None
    disclaimer: str
