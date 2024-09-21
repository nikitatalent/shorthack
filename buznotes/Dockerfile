FROM python:3.9-slim

# Установка зависимостей
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копирование кода приложения
COPY backend /app

WORKDIR /app

# Команда для запуска через Gunicorn
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "app:
