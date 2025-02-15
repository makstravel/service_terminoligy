#!/bin/sh

# Ожидание базы данных
echo "Ожидание базы данных..."
sleep 10

# Применение миграций
echo "Применение миграций..."
python manage.py migrate

# Сбор статических файлов (если нужно)
echo "Сбор статических файлов..."
python manage.py collectstatic --noinput

# Запуск сервера
echo "Запуск сервера..."
exec "$@"
