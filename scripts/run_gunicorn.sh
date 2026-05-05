#!/bin/bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

if [ ! -d "venv" ]; then
    echo "Virtual environment belum ada. Jalankan ./setup.sh atau siapkan venv production terlebih dahulu."
    exit 1
fi

if [ ! -f ".env" ]; then
    echo "File .env belum ada. Siapkan konfigurasi production sebelum menjalankan gunicorn."
    exit 1
fi

source venv/bin/activate

export APP_ENV="${APP_ENV:-production}"
export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-quiz_project.settings}"

HOST="${GUNICORN_HOST:-127.0.0.1}"
PORT="${GUNICORN_PORT:-8001}"
WORKERS="${GUNICORN_WORKERS:-3}"
TIMEOUT="${GUNICORN_TIMEOUT:-60}"
ACCESS_LOG="${GUNICORN_ACCESS_LOG:--}"
ERROR_LOG="${GUNICORN_ERROR_LOG:--}"

exec gunicorn \
    --bind "${HOST}:${PORT}" \
    --workers "${WORKERS}" \
    --timeout "${TIMEOUT}" \
    --access-logfile "${ACCESS_LOG}" \
    --error-logfile "${ERROR_LOG}" \
    quiz_project.wsgi:application
