# Используем Python образ
FROM python:3.11

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код из папки src
COPY src/ .

# Создаем директории для медиа файлов
RUN mkdir -p media

# Выполняем миграции и собираем статику
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Открываем порт
EXPOSE 8000

# Запускаем Gunicorn для Django
CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]