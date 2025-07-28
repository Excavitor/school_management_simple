@echo off
echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing Django and dependencies...
pip install django djangorestframework django-cors-headers djoser djangorestframework-simplejwt psycopg2-binary python-decouple

echo Creating Django project...
django-admin startproject school_management .

echo Creating Django apps...
python manage.py startapp accounts
python manage.py startapp public
python manage.py startapp dashboard

echo Initializing Git repository...
git init

echo Setup complete! Run 'venv\Scripts\activate.bat' to activate the virtual environment.