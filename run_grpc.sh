#!/bin/sh
# Запуск gRPC-сервиса рекомендаций (venv должен быть активирован): localhost:50051
cd "$(dirname "$0")" || exit 1
PYTHONPATH=db_service:grpc_service:proto exec python -m recommender.server
