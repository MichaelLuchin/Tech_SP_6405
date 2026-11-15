#!/bin/sh
# Запуск Notification Service (venv должен быть активирован): WebSocket ws://localhost:8001/ws
cd "$(dirname "$0")" || exit 1
PYTHONPATH=notification_service exec uvicorn notifier.main:app --host 0.0.0.0 --port 8001
