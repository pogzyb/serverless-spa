#!/usr/bin/env sh

mode=${APP_MODE}

if [[ $mode == "production" ]]; then
  echo "Running in production mode."
  uvicorn api.main:app \
    --workers 4 \
    --loop uvloop \
    --host 0.0.0.0 \
    --port ${APP_PORT} \
    --forwarded-allow-ips='*' \
    --proxy-headers
else
  echo "Running in non-production mode."
  uvicorn api.main:app \
    --reload \
    --host 0.0.0.0 \
    --port ${APP_PORT} \
    --log-level debug
fi
