#!/bin/sh
# Запуск nginx (reverse proxy) в Docker: http://localhost:8080 -> FastAPI на хосте :8000
cd "$(dirname "$0")" || exit 1
docker run --name nginx-proxy -p 8080:80 \
  --add-host=host.docker.internal:host-gateway \
  -v "$(pwd)/nginx/nginx.conf:/etc/nginx/nginx.conf:ro" \
  -v "$(pwd)/nginx/static:/usr/share/nginx/static:ro" \
  -d nginx:1.27-alpine
