# Используем Python образ
FROM python:3.11

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код из папки src
COPY src/ .

# Создаем директории
RUN mkdir -p media staticfiles

# Устанавливаем переменную окружения для STATIC_ROOT
ENV STATIC_ROOT=/app/staticfiles

# Выполняем миграции
RUN python manage.py migrate

# Собираем статику только если есть статические файлы
RUN python manage.py collectstatic --noinput --clear || echo "No static files to collect"

# Открываем порт
EXPOSE 8000

# Запускаем Gunicorn для Django
CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]