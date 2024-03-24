# Используем базовый образ Python
FROM python:3.9

# Устанавливаем переменную окружения для запуска в неинтерактивном режиме
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install fastapi uvicorn sqlalchemy asyncpg psycopg2-binary

# Копируем исходный код приложения в контейнер
COPY ./ /app

# Открываем порт, который будет использоваться в приложении
EXPOSE 9024

# Запускаем приложение при старте контейнера
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9024"]
