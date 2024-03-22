FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install requests psycopg2-binary djangorestframework

COPY . .

EXPOSE 8080

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8080"]