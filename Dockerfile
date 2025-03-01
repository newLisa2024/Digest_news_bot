FROM python:3.11-slim  # Базовый образ с Python 3.11
WORKDIR /app           # Рабочая директория внутри контейнера
COPY requirements.txt .  # Копируем файл зависимостей
RUN pip install --no-cache-dir -r requirements.txt  # Устанавливаем зависимости
COPY . .               # Копируем весь проект
CMD ["python", "-m", "bot"]  # Запускаем бота