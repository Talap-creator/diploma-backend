FROM python:3.10

# Установка рабочей директории в контейнере
WORKDIR /app

# Копирование файла зависимостей в рабочую директорию
COPY requirements.txt .

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода проекта в контейнер
COPY . .

# Запуск сервера Django на порту 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]