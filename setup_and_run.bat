@echo off
echo ============================================
echo   SMART REPAIR - Setup Script (Windows)
echo ============================================
echo.
echo [1/5] Creating virtual environment...
python -m venv venv
call venv\Scripts\activate
echo [2/5] Installing dependencies...
pip install -r requirements.txt
echo [3/5] Running database migrations...
python manage.py makemigrations accounts
python manage.py makemigrations core
python manage.py makemigrations bookings
python manage.py makemigrations payments
python manage.py makemigrations
python manage.py migrate
echo [4/5] Seeding database...
python manage.py seed_data
echo [5/5] Collecting static files...
python manage.py collectstatic --noinput
echo.
echo ============================================
echo   SETUP COMPLETE!
echo ============================================
echo.
echo  Browser: http://127.0.0.1:8000/
echo  Admin:   http://127.0.0.1:8000/admin/
echo  Login:   9999999999 / admin@123
echo  Emp IDs: EMP001-EMP015 / pass: emp@123
echo  OTP:     Check THIS terminal window!
echo.
python manage.py runserver
pause
