# SmartHabit

SmartHabit is a university machine-learning application that estimates smartphone-addiction risk from behavioural and demographic inputs. It is an educational prototype and does not provide a medical or psychological diagnosis.

## Container runtime

The image uses Python 3.12.13 on Debian Bookworm slim to match the model's recorded Python runtime. Runtime dependencies are installed from `requirements.txt`; pickle-critical scikit-learn and joblib versions are pinned to their recorded training versions.

The container serves both the FastAPI API and static frontend on port `8000`:

- Landing page: `http://localhost:8000/`
- Prediction page: `http://localhost:8000/predict.html`
- Health: `http://localhost:8000/api/health`
- Model information: `http://localhost:8000/api/model/info`
- API documentation: `http://localhost:8000/docs`

## Build and run

With Docker Engine or Docker Desktop running:

```bash
docker compose build
docker compose up -d
docker compose ps
```

Follow startup logs with:

```bash
docker compose logs -f smarthabit
```

Stop the application with:

```bash
docker compose down
```

## Verification

```bash
curl --fail http://localhost:8000/
curl --fail http://localhost:8000/api/health
curl --fail http://localhost:8000/api/model/info
curl --fail --request POST http://localhost:8000/api/predict \
  --header "Content-Type: application/json" \
  --data '{"age":24.0,"daily_screen_time_hours":6.5,"social_media_hours":2.5,"gaming_hours":1.0,"work_study_hours":3.0,"sleep_hours":7.0,"notifications_per_day":100.0,"app_opens_per_day":75.0,"weekend_screen_time":8.0,"gender":"Male","stress_level":"Medium","academic_work_impact":"Yes"}'
```

Inspect the health status and exact image size with:

```bash
docker inspect --format='{{.State.Health.Status}}' "$(docker compose ps -q smarthabit)"
docker image inspect smarthabit:1.0.0 --format='{{.Size}} bytes'
docker image ls smarthabit:1.0.0
```

## Runtime contents

The build context uses an allow-list. The image contains application source, static web assets, `docs/model-schema.json`, and only these model artifacts:

- `models/smartphone_addiction_model.joblib`
- `models/model_metadata.json`
- `models/environment.json`

Raw Kaggle data, notebooks, result outputs, submissions, screenshots, tests, local environments, caches, and secrets are excluded.

## Configuration

`docker-compose.yml` configures `APP_NAME`, `APP_VERSION`, `ENVIRONMENT`, `MODEL_PATH`, `METADATA_PATH`, `ALLOWED_ORIGINS`, and `MAX_REQUEST_BODY_BYTES`. Copy `.env.example` only for non-container local development; never commit a populated `.env` file.
