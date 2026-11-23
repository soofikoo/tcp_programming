#!/bin/sh
set -e

echo "[migrate] Применяю миграции..."
alembic upgrade head

echo "[seed] Заполняю базу..."
python fill_data.py

echo "[init] Готово!"