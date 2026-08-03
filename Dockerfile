FROM python:3.12.13-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update \
    && apt-get install --no-install-recommends -y curl libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./requirements.txt
RUN python -m pip install --no-cache-dir -r requirements.txt

RUN groupadd --system smarthabit \
    && useradd --system --gid smarthabit --home-dir /app --shell /usr/sbin/nologin smarthabit

COPY --chown=smarthabit:smarthabit api ./api
COPY --chown=smarthabit:smarthabit src ./src
COPY --chown=smarthabit:smarthabit web ./web
COPY --chown=smarthabit:smarthabit docs/model-schema.json ./docs/model-schema.json
COPY --chown=smarthabit:smarthabit models/smartphone_addiction_model.joblib ./models/smartphone_addiction_model.joblib
COPY --chown=smarthabit:smarthabit models/model_metadata.json ./models/model_metadata.json
COPY --chown=smarthabit:smarthabit models/environment.json ./models/environment.json

USER smarthabit

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD curl --fail --silent --show-error http://127.0.0.1:8000/api/health > /dev/null || exit 1

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--no-access-log"]
