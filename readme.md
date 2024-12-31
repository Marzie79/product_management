## Project Introduction

The management panel for **Product**

## Development Guide

- Python virtual environment (Optional)

  - Create a Python virtual environment:

  ```bash
  python -m venv venv
  ```

  - Activate the venv:

  ```bash
  source venv/bin/activate
  ```

  - Deactivate the venv:

  ```bash
  deactivate
  ```

  - Remove the venv:

  ```bash
  rm -rf venv
  ```

- Install project requirements:

  ```bash
  pip install -r requirements.txt
  ```

- Set Environment Variables:

  - Create .env file:

  ```bash
  cp .env.example .env
  ```

  - Set correct ENVs according to the your development environment in the `.env` file.

- Run app server:

  ```bash
  python manage.py runserver
  ```

- Django migrations:

  - Create migrations:

  ```bash
  python manage.py makemigrations
  ```

  - Apply migrations to the database:

  ```bash
  python manage.py migrate
  ```

- Create a superuser:

  ```bash
  python manage.py createsuperuser
  ```