#!/bin/bash

echo "🚀 ProQuiz Quick Start Script"
echo "=============================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file..."
    cat > .env << EOF
SECRET_KEY=django-insecure-change-me-in-production
DEBUG=True
DB_NAME=quiz
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=127.0.0.1
DB_PORT=5432
EOF
    echo "✅ .env file created"
fi

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate

# Check if superuser exists
echo "👤 Checking for superuser..."
python manage.py shell << EOF
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print('✅ Superuser created (admin/admin)')
else:
    print('✅ Superuser already exists')
EOF

# Populate sample data
echo "📊 Populating sample data..."
python manage.py shell < populate_data.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo "   1. Start server: python manage.py runserver"
echo "   2. Visit: http://127.0.0.1:8000/"
echo "   3. Admin: http://127.0.0.1:8000/admin/ (admin/admin)"
echo "   4. Test user: testuser/test123"
echo ""
echo "📚 Documentation:"
echo "   - README.md - Full documentation"
echo "   - IMPORT_GUIDE.md - CSV import guide"
echo "   - sample_questions.csv - CSV template"
echo ""
