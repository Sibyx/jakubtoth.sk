# jakubtoth.sk

Jakub Toth personal portfolio with administration using Django Admin.

## Install

We use [poetry](https://python-poetry.org/) for dependency management and [PostgreSQL](https://www.postgresql.org/) 17
(10+ should be compatible) as a data storage (acquisition files are stored on the filesystem, not in the database).
To set up instance with demo database follow these simple steps:

1. Create python virtual environment (`python -m venv venv`)
2. Enter environment (`source venv/bin/activate`)
3. Install dependencies `poetry install`
4. Create `.env` file according `.env.example`
5. Execute migrations `python manage.py migrate`
6. Create superuser using `python manage.py createsuperuser`

---
Made with ❤️ and ☕️ Jakub Dubec (c) 2022-2025
