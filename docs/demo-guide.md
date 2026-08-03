# SmartHabit five-minute demonstration guide

## Before the demonstration

Choose one startup method and confirm port 8000 is free.

### Local startup

From the repository root in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
python -m uvicorn api.main:app --host 127.0.0.1 --port 8000
```

### Docker startup

With Docker Desktop or Docker Engine running:

```powershell
docker compose build
docker compose up -d
docker compose ps
```

Docker was not available in the documentation environment. Run the container verification in the final demonstration environment before presenting it as completed evidence.

## Five-minute script

### 0:00–0:40 — Introduce the project

Open <http://127.0.0.1:8000/>.

Say:

> SmartHabit is my CIS6005 Computational Intelligence project. It uses a saved LightGBM pipeline from the Kaggle Playground Series Season 6, Episode 8 smartphone-addiction competition. It estimates a probability from usage patterns for educational reflection. It is not a medical or psychological diagnosis.

Point out the privacy, AI, and responsible-use messages. Do not call the Kaggle score clinical accuracy.

### 0:40–1:30 — Show the prediction form

Open <http://127.0.0.1:8000/predict.html>.

Explain:

- the frontend fetches the model schema from `GET /api/model/schema`;
- it builds controls for exactly 12 raw fields and never sends `id`;
- numeric bounds and categories are enforced in both the browser and Pydantic;
- the form includes keyboard focus, inline errors, loading state, and a non-diagnostic disclaimer.

Briefly submit an invalid value or omit a field to show validation without exposing internal details.

### 1:30–2:35 — Run a real prediction

Use the Moderate example below. Select **Predict Your Risk**.

Explain the flow:

> The API validates the request, creates a one-row DataFrame, calls the shared feature-engineering function, and passes the 16 ordered features into the saved preprocessing and LightGBM pipeline. It uses `predict_proba` and verifies the positive class instead of assuming a class index.

The verified result for this payload is Moderate with addiction probability approximately **0.4914**. Small differences should not be claimed without rerunning the saved artifact and pinned runtime.

### 2:35–3:20 — Explain the result dashboard

Point out:

- addiction and non-addiction probabilities;
- predicted class;
- Low, Moderate, and High display bands;
- the highlighted current band;
- model version shown as unavailable/not recorded because metadata contains no version;
- the educational disclaimer; and
- the print-friendly report layout.

State that the thresholds are interface display choices, not clinical thresholds.

### 3:20–4:05 — Explain local model factors

Show **Model factors influencing this prediction**.

Say:

> These are local LightGBM contribution values for this prediction. One-hot columns are grouped into readable names. Direction shows movement toward a higher or lower model estimate. The magnitude is normalized only for display; it is not a percentage cause and the factors do not establish causality.

Mention that explanation failure does not block prediction; the API returns an `unavailable` fallback.

### 4:05–4:40 — Show the API and model evidence

Open:

- <http://127.0.0.1:8000/docs>
- <http://127.0.0.1:8000/api/model/info>
- <http://127.0.0.1:8000/model.html>

Explain the verified results:

- holdout ROC AUC: `0.9597828493`;
- three-fold mean ROC AUC: `0.9603813962 ± 0.0004852321`; and
- Kaggle public leaderboard ROC AUC: `0.96189`.

Call each one ROC AUC, not accuracy.

### 4:40–5:00 — Close responsibly

Open <http://127.0.0.1:8000/disclaimer.html>.

Say:

> The main limitations are competition-data representativeness, self-reported inputs, distribution shift, and the risk of treating probability as certainty. The tool is intended for education and reflection only and must not be used for diagnosis, treatment, or high-impact decisions.

## Verified demonstration inputs

These payloads were executed against the repository's real saved model during documentation verification. They are demonstration examples, not profiles of real people and not clinical scenarios.

### Low example

```json
{
  "age": 26.0,
  "daily_screen_time_hours": 7.4,
  "social_media_hours": 1.82,
  "gaming_hours": 2.68,
  "work_study_hours": 2.62,
  "sleep_hours": 8.25,
  "notifications_per_day": 50.0,
  "app_opens_per_day": 119.0,
  "weekend_screen_time": 5.84,
  "gender": "Other",
  "stress_level": "Medium",
  "academic_work_impact": "Yes"
}
```

Verified output: class `0`, addiction probability `0.09928293860835534`, Low.

### Moderate example

```json
{
  "age": 29.0,
  "daily_screen_time_hours": 1.63,
  "social_media_hours": 0.24,
  "gaming_hours": 1.39,
  "work_study_hours": 0.11,
  "sleep_hours": 5.24,
  "notifications_per_day": 93.0,
  "app_opens_per_day": 124.0,
  "weekend_screen_time": 12.58,
  "gender": "Other",
  "stress_level": "High",
  "academic_work_impact": "Yes"
}
```

Verified output: class `0`, addiction probability `0.49141790955455894`, Moderate.

### High example

```json
{
  "age": 19.0,
  "daily_screen_time_hours": 6.86,
  "social_media_hours": 6.87,
  "gaming_hours": 2.79,
  "work_study_hours": 0.57,
  "sleep_hours": 8.89,
  "notifications_per_day": 198.0,
  "app_opens_per_day": 137.0,
  "weekend_screen_time": 13.91,
  "gender": "Other",
  "stress_level": "Low",
  "academic_work_impact": "No"
}
```

Verified output: class `1`, addiction probability `0.9996223087822702`, High.

## API verification commands

PowerShell uses `curl.exe` to avoid the `Invoke-WebRequest` alias:

```powershell
curl.exe --fail http://127.0.0.1:8000/api/health
curl.exe --fail http://127.0.0.1:8000/api/model/info
curl.exe --fail http://127.0.0.1:8000/api/model/schema
curl.exe --fail --request POST http://127.0.0.1:8000/api/predict --header "Content-Type: application/json" --data '{"age":29.0,"daily_screen_time_hours":1.63,"social_media_hours":0.24,"gaming_hours":1.39,"work_study_hours":0.11,"sleep_hours":5.24,"notifications_per_day":93.0,"app_opens_per_day":124.0,"weekend_screen_time":12.58,"gender":"Other","stress_level":"High","academic_work_impact":"Yes"}'
```

## Code files to explain

| File | Talking point |
|---|---|
| `src/feature_engineering.py` | Copy-on-write domain features and zero-denominator behavior |
| `api/schemas.py` | Exact fields, finite values, ranges, categories, and forbidden extras |
| `api/model_loader.py` | One-time trusted loading, version checks, feature-order checks |
| `api/predictor.py` | DataFrame → features → pipeline → class/probability → risk band |
| `api/explainer.py` | Local LightGBM contributions, one-hot grouping, fallback |
| `api/main.py` | Lifespan, CORS, middleware, routers, and static frontend mount |
| `api/middleware.py` | Body limit, request IDs, structured logging, security headers |
| `web/js/prediction.js` | Dynamic fields, accessible validation, result and factor rendering |
| `tests/test_prediction.py` | Real model integration and safe error behavior |
| `Dockerfile` | Pinned Python runtime, allow-listed artifacts, non-root execution |

## Screenshots to capture

Save screenshots in `screenshots/` without fabricating or editing result values:

1. `landing-page.png` — full landing page at desktop width.
2. `prediction-form.png` — populated form before submission.
3. `validation-error.png` — inline missing/invalid-field feedback.
4. `prediction-low.png` — real Low result and highlighted green card.
5. `prediction-moderate.png` — real Moderate result and highlighted amber card.
6. `prediction-high.png` — real High result and highlighted red card.
7. `prediction-factors.png` — local factors label, directions, magnitudes, and limitation.
8. `swagger-api.png` — Swagger UI showing the four JSON API endpoints.
9. `model-info.png` — safe model metadata JSON.
10. `pytest-passed.png` — terminal showing the complete passing suite.
11. `docker-health.png` — final container status and health check after Docker verification.
12. `responsive-mobile.png` — prediction page at a mobile viewport.

Ensure screenshots do not display local absolute paths, `.env` contents, secrets, unrelated browser tabs, or personal notifications.

## Test command

```powershell
pytest -q
python -m compileall -q api src
```

Expected result for the current repository: 39 tests passed and no compilation errors.
