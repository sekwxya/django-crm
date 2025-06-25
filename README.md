# Furry CRM

CRM-система со складским учётом на Django

## Функциональность

- Авторизация и регистрация пользователей с ролями
- Управление складом и товарами
- Ведение заявок клиентов
- Управление клиентами
- Формирование отчетов

## Требования

- Python 3.8+
- PostgreSQL 13+
- pip (Python package manager)

## Установка и запуск

1. Создайте виртуальное окружение:
```bash 
python -m venv venv # или python3 -m venv venv
```

2. Активируйте виртуальное окружение:
- Windows: 
```bash
venv\Scripts\activate
```
- Linux/MacOS:
```bash
source venv/bin/activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

```bash
psql -U postgres -h localhost
```
Введите пароль пользователя postgres
```bash
your_password
```

4. Создайте базу данных PostgreSQL:
```bash
CREATE DATABASE furry_crm;
CREATE USER furry_crm_user WITH PASSWORD 'your_password';
ALTER ROLE furry_crm_user SET client_encoding TO 'utf8';
ALTER ROLE furry_crm_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE furry_crm_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE furry_crm TO furry_crm_user;
GRANT ALL ON SCHEMA public TO furry_crm_user;
```

5. Создайте файл .env в корневой директории проекта со следующими параметрами (Необходимо сгенерировать secret key, db_password - от пароля furry_crm_user созданного пунктом ранее):
```
DEBUG=True
SECRET_KEY=your-secret-key
DB_NAME=furry_crm
DB_USER=furry_crm_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

```
pip install psycopg
```

6. Примените миграции:
```bash
python manage.py migrate
```

7. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

8. Запустите сервер разработки:
```bash
python manage.py runserver
```

## Технологии

- Python 3.8+
- Django 5.0
- PostgreSQL (база данных)
- Bootstrap 5 (фронтенд) 