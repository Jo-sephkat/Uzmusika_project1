#!/bin/bash
set -e
echo "🚀 Starting Django build process..."
pip install -r requirements.txt
pip install whitenoise
python manage.py collectstatic --noinput --clear
python manage.py makemigrations --noinput
python manage.py migrate --noinput
echo "✅ Build completed successfully!"


