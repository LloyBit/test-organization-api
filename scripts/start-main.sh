#!/usr/bin/env bash
set -e

# Запуск миграций
echo "Запуск миграций..."

# Устанавливаем PYTHONPATH 
export PYTHONPATH="$(dirname "$(dirname "$0")")"

if alembic upgrade head; then
  echo "Миграции завершены успешно!"
else
  echo "Миграции не выполнены!"
  exit 1
fi

# Заполнение базы данных тестовыми данными
echo "Заполнение базы данных..."
python -m app.fill_db

# Запуск приложения
exec uvicorn app.main:app --host 0.0.0.0 --port 8000