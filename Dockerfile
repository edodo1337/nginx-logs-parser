FROM python:3.12-slim

WORKDIR /app
COPY src/ ./src/
COPY README.md ./
COPY pyproject.toml ./
RUN apt-get update && apt-get install -y clang libpq-dev python3-dev gcc
COPY requirements.lock requirements-dev.lock ./
RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -r requirements.lock
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=app.settings

COPY .env .env
RUN python src/manage.py migrate

CMD ["gunicorn", "--chdir", "src", "app.wsgi:application", "--bind", "0.0.0.0:8000"]
