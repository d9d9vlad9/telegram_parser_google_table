#!/bin/bash
echo "🔄 Останавливаю контейнеры..."
docker-compose down

echo "⬆️ Обновляю pip в контейнере и пересобираю образ..."
docker-compose build --no-cache

echo "🚀 Запускаю контейнеры..."
docker-compose up -d

echo "📜 Логи (последние 60 строк):"
docker-compose logs --tail=60
