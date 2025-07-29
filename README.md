## .env file
```bash
DEBUG=True
SECRET_KEY=
USE_SQLITE=False
DATABASE_NAME=school_management_system_django
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_HOST=localhost
DATABASE_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
```

## How to RUN

- Clone The Repo
- Create Virtual Environment
- Install Dependences `pip install -r requirements.txt`
- Create Database
- Make Migrations `python manage.py makemigrations`
- Migrate Database `python manage.py migrate`
- Create Superuser `python manage.py createsuperuser`
- Run Server `python manage.py runserver`