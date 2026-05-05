#!/bin/bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

if [ ! -d "venv" ]; then
    echo "Virtual environment belum ada. Buat venv production terlebih dahulu."
    exit 1
fi

if [ ! -f ".env" ]; then
    echo "File .env belum ada. Salin dari .env.example atau deploy/.env.production.example lalu isi nilainya."
    exit 1
fi

source venv/bin/activate

export APP_ENV="${APP_ENV:-production}"
export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-quiz_project.settings}"

if command -v npm >/dev/null 2>&1; then
    echo "Installing frontend dependencies..."
    npm install --silent

    echo "Building CSS bundle..."
    npm run build:css >/dev/null
fi

echo "Installing dependencies..."
pip install -q -r requirements.txt

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Running deployment checks..."
python manage.py check --deploy

echo ""
echo "Production build step selesai."
echo "Langkah berikutnya:"
echo "1. Pastikan service gunicorn aktif"
echo "2. Pastikan reverse proxy nginx mengarah ke port gunicorn"
echo "3. Verifikasi /healthz dan login admin"
