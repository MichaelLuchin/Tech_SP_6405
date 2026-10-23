#!/bin/sh
# Запуск API Service (venv должен быть активирован): http://localhost:8000/docs
cd "$(dirname "$0")" || exit 1
PYTHONPATH=db_service:api_service exec uvicorn api.main:app \
  --host 0.0.0.0 --port 8000 \
  --reload --reload-dir api_service --reload-dir db_service
