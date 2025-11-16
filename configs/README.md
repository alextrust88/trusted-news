# Конфигурационные файлы

Эта директория содержит конфигурационные файлы для различных компонентов системы.

## Файлы

### `alloy.config.river`

Конфигурация Grafana Alloy для сбора и отправки метрик в Grafana Cloud.

**Использование:**
- Копируется на сервер при деплое
- Монтируется в контейнер `grafana-alloy` через docker-compose

**Переменные окружения:**
- `GCLOUD_HOSTED_METRICS_URL` - URL для отправки метрик
- `GCLOUD_HOSTED_METRICS_ID` - ID метрик в Grafana Cloud
- `GCLOUD_RW_API_KEY` - API ключ для записи метрик

## Добавление новых конфигураций

При добавлении новых конфигурационных файлов:

1. Разместите их в этой директории
2. Обновите `.dockerignore` если нужно
3. Обновите `docker-compose.yml` и `docker-compose.prod.yml` для монтирования
4. Обновите workflow в `.github/workflows/ci-cd.yml` для копирования на сервер


