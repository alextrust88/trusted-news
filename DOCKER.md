# Инструкция по запуску в Docker

## Требования

- Docker (версия 20.10+)
- Docker Compose (версия 1.29+)

## Быстрый старт

1. **Создайте файл `.env`** с вашими токенами:
```bash
TELEGRAM_BOT_TOKEN=ваш_токен
TELEGRAM_CHAT_ID=ваш_chat_id
```

2. **Запустите контейнер:**
```bash
# Только бот
docker-compose up -d

# Бот + Grafana Alloy (для метрик)
docker-compose --profile monitoring up -d
```

3. **Проверьте логи:**
```bash
docker-compose logs -f
```

4. **Остановите контейнер:**
```bash
docker-compose down
```

## Сборка образа вручную

Если хотите собрать образ без docker-compose:

```bash
# Сборка образа
docker build -t newsagent .

# Запуск контейнера
docker run -d \
  --name newsagent-bot \
  --env-file .env \
  --restart unless-stopped \
  newsagent

# Просмотр логов
docker logs -f newsagent-bot

# Остановка и удаление
docker stop newsagent-bot
docker rm newsagent-bot
```

## Переменные окружения

Переменные можно передать двумя способами:

1. **Через файл `.env`** (рекомендуется):
```bash
docker-compose up -d
```

2. **Через переменные окружения напрямую**:
```bash
docker run -d \
  --name newsagent-bot \
  -e TELEGRAM_BOT_TOKEN=ваш_токен \
  -e TELEGRAM_CHAT_ID=ваш_chat_id \
  newsagent
```

## Отладка

Если что-то не работает:

1. Проверьте логи:
```bash
docker-compose logs
```

2. Запустите контейнер в интерактивном режиме:
```bash
docker-compose run --rm newsagent sh
```

3. Проверьте переменные окружения внутри контейнера:
```bash
docker-compose exec newsagent env | grep TELEGRAM
```

## Обновление

Для обновления кода:

```bash
# Остановите контейнер
docker-compose down

# Пересоберите образ
docker-compose build

# Запустите заново
docker-compose up -d
```

## Автоматический перезапуск

Контейнер настроен на автоматический перезапуск при сбоях (`restart: unless-stopped`).

Если нужно отключить:
```yaml
# В docker-compose.yml измените:
restart: "no"
```

