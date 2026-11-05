#!/bin/sh
# Генерация Python-кода из proto/recommendations.proto (venv должен быть активирован)
cd "$(dirname "$0")" || exit 1
python -m grpc_tools.protoc -I proto \
  --python_out=proto --grpc_python_out=proto \
  proto/recommendations.proto
