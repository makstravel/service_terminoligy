# Используем Python 3.11
FROM python:3.11

# Устанавливаем переменные окружения
ENV PYTHONWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Указываем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc libpq-dev gettext curl && \
    rm -rf /var/lib/apt/lists/*

# Обновляем pip
RUN pip install --upgrade pip

# Копируем зависимости
COPY requirements11.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements11.txt

# Копируем все файлы проекта
COPY . .

# Указываем настройки Django
ENV DJANGO_SETTINGS_MODULE=config.settings

# Добавляем точку входа
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
