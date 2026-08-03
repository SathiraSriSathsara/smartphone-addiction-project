# SmartHabit

SmartHabit is a university machine-learning application for the **CIS6005 Computational Intelligence** module (student ID **20302367**). It uses a saved LightGBM pipeline to estimate the probability of the Kaggle target `addicted_label` from smartphone-use, work/study, sleep, stress, and demographic inputs.

This is an educational prototype. It does not diagnose smartphone addiction or any medical or psychological condition.

## Screenshots

> Replace these placeholders with final deployment screenshots captured using the checklist in `docs/demo-guide.md`.

| Landing page | Prediction form |
|---|---|
| `screenshots/landing-page.png` *(placeholder)* | `screenshots/prediction-form.png` *(placeholder)* |

| Prediction result | API documentation |
|---|---|
| `screenshots/prediction-result.png` *(placeholder)* | `screenshots/swagger-api.png` *(placeholder)* |

## Features

- Responsive landing, prediction, project, model, and disclaimer pages using plain HTML, CSS, and JavaScript.
- Dynamic prediction form sourced from `GET /api/model/schema`.
- Strict Pydantic validation for the exact 12 raw model inputs.
- Shared, training-compatible feature engineering that creates four derived features.
- Singleton loading of the trusted local joblib pipeline at application startup.
- LightGBM probability prediction with verified positive-class mapping.
- Low, Moderate, and High non-clinical display bands.
- Per-prediction LightGBM contribution explanation with up to five readable factors and a safe fallback.
- Request-size protection, restricted CORS, request IDs, structured logging, safe errors, and security headers.
- FastAPI Swagger and ReDoc documentation.
- Automated tests and a single-port container configuration.

## Verified project facts

| Item | Verified value |
|---|---|
| Competition | Predicting Smartphone Addiction — Playground Series Season 6, Episode 8 |
| Selected model | LightGBM |
| Target | `addicted_label` |
| Official metric | ROC AUC |
| Final training rows | 691,369 |
| Model input columns | 16: 12 raw and four engineered |
| Holdout ROC AUC | 0.9597828493 |
| Three-fold mean ROC AUC | 0.9603813962 ± 0.0004852321 |
| Kaggle public leaderboard ROC AUC | 0.96189 |

The scores above are competition evaluation results, not clinical accuracy or diagnostic validity.

## Repository structure

```text
smartphone-addiction-project/
├── api/                  # FastAPI app, routes, model service, prediction and security
├── data/                 # Original Kaggle data; excluded from containers and Git
├── docs/                 # Architecture, API, model, demo and audit documentation
├── models/               # Saved pipeline and audited runtime metadata
├── notebooks/            # Executed training and evaluation notebook
├── outputs/              # Verified figures, results and Kaggle submission evidence
├── screenshots/          # Assignment evidence images
├── src/                  # Shared feature engineering
├── tests/                # Pytest unit and integration tests
├── web/                  # Static HTML, CSS, JavaScript and image assets
├── .dockerignore
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── pytest.ini
├── requirements.txt
└── README.md
```

## Local setup

The model was saved with Python 3.12.13. Use Python 3.12 and the pinned dependencies where possible.

PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

The example environment restricts browser origins to local development addresses. Do not set `ALLOWED_ORIGINS=*`.

## Local execution

Run from the repository root so relative model and web paths resolve correctly:

```powershell
python -m uvicorn api.main:app --host 127.0.0.1 --port 8000
```

Open:

- Landing page: <http://127.0.0.1:8000/>
- Prediction page: <http://127.0.0.1:8000/predict.html>
- Swagger UI: <http://127.0.0.1:8000/docs>
- Health endpoint: <http://127.0.0.1:8000/api/health>

The model is loaded once during FastAPI lifespan startup. Startup fails if required artifacts are absent or a pickle-critical package version is unsafe.

## Docker execution

With Docker Engine or Docker Desktop running:

```powershell
docker compose build
docker compose up -d
docker compose ps
```

The frontend and API use one exposed port: <http://localhost:8000/>.

Verify and stop:

```powershell
curl.exe --fail http://localhost:8000/
curl.exe --fail http://localhost:8000/api/health
curl.exe --fail http://localhost:8000/api/model/info
docker inspect --format='{{.State.Health.Status}}' (docker compose ps -q smarthabit)
docker image inspect smarthabit:1.0.0 --format='{{.Size}} bytes'
docker compose down
```

The image uses `python:3.12.13-slim-bookworm`, runs as a non-root user, uses a read-only root filesystem through Compose, and includes only runtime source, web assets, the model schema, and three required model artifacts. Raw data, notebooks, outputs, screenshots, tests, caches, and local secrets are excluded.

Docker was unavailable in the documentation environment, so these Docker commands remain deployment verification steps rather than claimed execution results.

## Testing

```powershell
pytest -q
python -m compileall -q api src
```

The verified documentation-pass result is **39 tests passed**. Tests cover health and static serving, model loading, feature engineering, validation, predictions, local explanations, safe errors, CORS configuration, body limits, request IDs, and security headers.

## Configuration

| Variable | Default/example | Purpose |
|---|---|---|
| `APP_NAME` | `SmartHabit API` | Public API title |
| `APP_VERSION` | `1.0.0` | Application version |
| `ENVIRONMENT` | `development` | Runtime environment; production enables HSTS |
| `MODEL_PATH` | `models/smartphone_addiction_model.joblib` | Trusted model path |
| `METADATA_PATH` | `models/model_metadata.json` | Model metadata path |
| `ALLOWED_ORIGINS` | Local port 5500 origins | Explicit comma-separated CORS origins |
| `MAX_REQUEST_BODY_BYTES` | `16384` | Maximum request body size |

## Limitations

- Competition data may not represent every population, culture, age group, or real-world usage context.
- Inputs are self-reported and may be approximate or biased.
- ROC AUC and leaderboard scores do not establish clinical validity.
- Risk bands are application display thresholds, not clinical thresholds.
- Explanations describe model influence, not causes or treatment priorities.
- The original LightGBM training version was not recorded; runtime 4.7.0 has been tested locally.
- The saved metadata does not contain a model version, so API responses return `null` for `model_version`.
- No user accounts or application database are implemented. Deployment operators may still retain infrastructure access logs.
- Rate limiting is expected to be applied at the deployment boundary if publicly exposed.

## Technical documentation

- [Architecture](docs/architecture.md)
- [API reference](docs/api.md)
- [Model card](docs/model-card.md)
- [Five-minute demo guide](docs/demo-guide.md)
- [Quality report](docs/quality-report.md)
- [Repository audit](docs/repository-audit.md)
