#!/bin/bash
echo "============================================"
echo "  SMART REPAIR - Setup Script (Linux/Mac)"
echo "============================================"
echo "[1/5] Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate
echo "[2/5] Installing dependencies..."
pip install -r requirements.txt
echo "[3/5] Running migrations..."
python manage.py makemigrations accounts
python manage.py makemigrations core
python manage.py makemigrations bookings
python manage.py makemigrations payments
python manage.py makemigrations
python manage.py migrate
echo "[4/5] Seeding database with 99 AP centers, repair issues, workers..."
python manage.py seed_data
echo "[5/5] Collecting static..."
python manage.py collectstatic --noinput
echo ""
echo "=== SETUP COMPLETE ==="
echo "Browser: http://127.0.0.1:8000/"
echo "Admin:   http://127.0.0.1:8000/admin/ → 9999999999 / admin@123"
echo "Employee: EMP001-EMP015 / emp@123"
echo "OTP: Check THIS terminal!"
echo ""
python manage.py runserver
