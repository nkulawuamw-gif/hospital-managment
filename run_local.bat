@echo off
cd /d "%~dp0"

echo ============================================
echo  HMS - Hospital Management System
echo  Starting local development server...
echo ============================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Apply any pending migrations
echo [1/3] Applying migrations...
python manage.py migrate

REM Collect static files
echo [2/3] Collecting static files...
python manage.py collectstatic --noinput --clear >nul 2>&1

REM Start development server
echo [3/3] Starting server...
echo.
echo  Access the application at: http://localhost:8000
echo  Admin login: admin@hospital.com / Admin@123
echo  Press Ctrl+C to stop
echo ============================================
echo.

python manage.py runserver localhost:8000

pause
