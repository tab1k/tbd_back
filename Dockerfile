# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем и устанавливаем зависимости
COPY ./tbd_back/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код из папки src
COPY ./tbd_back/src/ .

# Собираем статику для Django (если нужно)
RUN python manage.py collectstatic --noinput

# Открываем порт
EXPOSE 8000

# Запускаем Gunicorn для Django
CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]
