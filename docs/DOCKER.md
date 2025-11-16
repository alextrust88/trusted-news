# Инструкция по запуску в Docker

## Требования

- Docker (версия 20.10+)
- Docker Compose (версия 1.29+) или Docker Compose Plugin

## Быстрый старт

### Для разработки (локально)

1. **Создайте файл `.env`** в корне проекта с вашими токенами:
```bash
TELEGRAM_BOT_TOKEN=ваш_токен
TELEGRAM_CHAT_ID=ваш_chat_id
METRICS_PORT=8000

# Опционально: для Grafana Alloy
GCLOUD_HOSTED_METRICS_URL=ваш_url
GCLOUD_HOSTED_METRICS_ID=ваш_id
GCLOUD_RW_API_KEY=ваш_ключ
```

2. **Запустите все контейнеры:**
```bash
# Перейдите в директорию docker
cd docker

# Запуск всех сервисов (бот + парсер)
docker compose up -d

# Или с Grafana Alloy для мониторинга метрик
docker compose --profile monitoring up -d
```

**Сервисы:**
- `newsagent` - Telegram бот (Python)
- `parser` - Парсер новостей (Go)
- `grafana-alloy` - Сбор метрик (только с профилем `monitoring`)

3. **Проверьте статус контейнеров:**
```bash
docker compose ps
```

4. **Просмотрите логи:**
```bash
# Все логи
docker compose logs -f

# Логи конкретного сервиса
docker compose logs -f newsagent
docker compose logs -f parser
docker compose logs -f grafana-alloy
```

5. **Остановите контейнеры:**
```bash
docker compose down
```

### Для продакшена

1. **На сервере создайте файл `.env`** в директории проекта

2. **Запустите все контейнеры:**
```bash
cd /opt/newsagent  # или ваша директория
docker compose -f docker/docker-compose.prod.yml up -d
```

**Примечание:** В продакшене все сервисы запускаются автоматически, включая Grafana Alloy.

## Сборка образов вручную

Если хотите собрать образы без docker-compose:

```bash
# Сборка образа бота
docker build -t newsagent -f src/bot/Dockerfile .

# Сборка образа парсера
docker build -t newsagent-parser -f src/parser/Dockerfile .

# Запуск контейнеров
docker run -d \
  --name newsagent-bot \
  --env-file .env \
  --restart unless-stopped \
  -p 8000:8000 \
  newsagent

docker run -d \
  --name newsagent-parser \
  --env-file .env \
  --restart unless-stopped \
  newsagent-parser

# Просмотр логов
docker logs -f newsagent-bot
docker logs -f newsagent-parser

# Остановка и удаление
docker stop newsagent-bot newsagent-parser
docker rm newsagent-bot newsagent-parser
```

## Переменные окружения

**Важно:** Бот всегда читает переменные из окружения Docker. Файл `.env` используется только для локальной разработки.

### В Docker Compose

Переменные передаются через секцию `env_file` в `docker-compose.yml`:

```yaml
services:
  newsagent:
    env_file:
      - ../.env  # Docker Compose автоматически загружает переменные из файла
    environment:
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}  # Или напрямую через environment
```

Docker Compose автоматически:
1. Читает переменные из `.env` файла
2. Передает их в контейнер как переменные окружения
3. Бот читает их через `os.getenv()`

### Локальная разработка (без Docker)

Для локального запуска экспортируйте переменные окружения:

```bash
export TELEGRAM_BOT_TOKEN=ваш_токен
export TELEGRAM_CHAT_ID=ваш_chat_id

cd src/bot
uv run python simple_bot.py
```

Или установите переменные в текущей сессии:

```bash
TELEGRAM_BOT_TOKEN=ваш_токен TELEGRAM_CHAT_ID=ваш_chat_id uv run python simple_bot.py
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
# Остановите контейнеры
docker compose down

# Пересоберите образы
docker compose build

# Или пересоберите конкретный сервис
docker compose build newsagent
docker compose build parser

# Запустите заново
docker compose up -d
```

## Полезные команды

### Просмотр статуса всех сервисов
```bash
docker compose ps
```

### Перезапуск конкретного сервиса
```bash
docker compose restart newsagent
docker compose restart parser
docker compose restart grafana-alloy
```

### Просмотр логов конкретного сервиса
```bash
docker compose logs -f newsagent
docker compose logs -f parser
docker compose logs -f grafana-alloy
```

### Выполнение команд внутри контейнера
```bash
# Войти в контейнер бота
docker compose exec newsagent sh

# Выполнить команду в контейнере парсера
docker compose exec parser /app/parser --help
```

### Проверка метрик
```bash
# Метрики бота
curl http://localhost:8000/metrics

# UI Grafana Alloy (если запущен с профилем monitoring)
open http://localhost:12345
```

## Автоматический перезапуск

Контейнер настроен на автоматический перезапуск при сбоях (`restart: unless-stopped`).

Если нужно отключить:
```yaml
# В docker-compose.yml измените:
restart: "no"
```

## Устранение проблем

### Ошибка: "The container name ... is already in use"

Если контейнер с таким именем уже существует:

```bash
# Остановите и удалите все контейнеры проекта
cd docker
docker compose down

# Или удалите конкретный контейнер вручную
docker rm -f newsagent-bot
docker rm -f newsagent-parser
docker rm -f grafana-alloy

# Затем запустите заново
docker compose up -d
```

### Очистка всех контейнеров и volumes

```bash
cd docker
docker compose down -v  # Удаляет также volumes
docker compose rm -f    # Принудительное удаление остановленных контейнеров
```

### Проверка существующих контейнеров

```bash
# Список всех контейнеров проекта
docker ps -a --filter "name=newsagent"

# Удаление всех контейнеров проекта
docker rm -f $(docker ps -a --filter "name=newsagent" -q)
```

