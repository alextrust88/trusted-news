# Docker Compose конфигурации

## Быстрый старт

### 1. Создайте файл `.env` в корне проекта

```bash
# Из корня проекта
cp .env.example .env

# Отредактируйте .env и добавьте ваши токены
nano .env  # или используйте любой редактор
```

### 2. Запустите контейнеры

```bash
# Из директории docker/
docker compose up -d

# Или с Grafana Alloy для мониторинга
docker compose --profile monitoring up -d
```

## Структура файлов

- `docker-compose.yml` - для локальной разработки
- `docker-compose.prod.yml` - для продакшена

## Важно

Файл `.env` должен находиться в **корне проекта** (не в директории `docker/`), так как:
- `docker-compose.yml` использует `context: ..` (корень проекта)
- `env_file: ../.env` указывает на корень проекта относительно `docker/`

## Переменные окружения

Минимально необходимые переменные в `.env`:

```bash
TELEGRAM_BOT_TOKEN=ваш_токен
TELEGRAM_CHAT_ID=ваш_chat_id
METRICS_PORT=8000
```

Для Grafana Alloy (опционально):

```bash
GCLOUD_HOSTED_METRICS_URL=ваш_url
GCLOUD_HOSTED_METRICS_ID=ваш_id
GCLOUD_RW_API_KEY=ваш_ключ
```

## Устранение проблем

### Ошибка: "env file .../.env not found"

1. Убедитесь, что файл `.env` существует в корне проекта:
   ```bash
   ls -la ../.env
   ```

2. Если файла нет, создайте его из примера:
   ```bash
   cp ../.env.example ../.env
   ```

3. Заполните необходимые переменные в `.env`

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

### Очистка всех контейнеров проекта

```bash
cd docker
docker compose down -v  # Удаляет также volumes
docker compose rm -f    # Принудительное удаление
```

