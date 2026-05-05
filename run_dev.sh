#!/bin/bash

set -e

echo "🚀 ProQuiz Dev Runner"
echo "===================="
echo ""

if [ ! -d "venv" ]; then
    echo "Virtual environment belum ada. Jalankan ./setup.sh terlebih dahulu."
    exit 1
fi

if [ ! -f ".env" ]; then
    echo "⚙️  Membuat .env dari .env.example..."
    cp .env.example .env
fi

echo "🔧 Activating virtual environment..."
source venv/bin/activate

echo "🗄️  Running migrations..."
python manage.py migrate

pick_port() {
    local port=8000

    while command -v lsof >/dev/null 2>&1 && lsof -nP -iTCP:${port} -sTCP:LISTEN >/dev/null 2>&1; do
        port=$((port + 1))
    done

    echo "${port}"
}

PORT="$(pick_port)"

echo ""
if [ "${PORT}" != "8000" ]; then
    echo "ℹ️  Port 8000 sedang dipakai. Mengalihkan ke port ${PORT}."
fi

echo "🌐 Starting development server at http://127.0.0.1:${PORT}/"
python manage.py runserver 127.0.0.1:${PORT}
