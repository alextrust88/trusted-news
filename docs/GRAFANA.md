# Настройка метрик с Grafana Alloy

Проект использует Grafana Alloy для отправки метрик в Grafana Cloud.

## Архитектура

```
NewsAgent Bot → Prometheus Metrics Endpoint (port 8000)
                    ↓
            Grafana Alloy (скрапит метрики)
                    ↓
            Grafana Cloud (Prometheus)
```

## Настройка Grafana Cloud

1. **Создайте аккаунт в Grafana Cloud** (если еще нет):
   - Перейдите на https://grafana.com/auth/sign-up/create-user
   - Создайте бесплатный аккаунт

2. **Создайте Prometheus instance**:
   - В Grafana Cloud перейдите в раздел "My Account" → "Prometheus"
   - Создайте новый instance или используйте существующий
   - Скопируйте:
     - **Remote Write URL** (например: `https://prometheus-prod-XX-prod.grafana.net/api/prom/push`)
     - **Instance ID** (username)
     - **API Key** (password)

3. **Настройте переменные окружения** в `.env`:
```bash
GRAFANA_CLOUD_REMOTE_WRITE_URL=https://prometheus-prod-XX-prod.grafana.net/api/prom/push
GRAFANA_CLOUD_USERNAME=your_instance_id
GRAFANA_CLOUD_PASSWORD=your_api_key
```

## Запуск с Grafana Alloy

### Вариант 1: Docker Compose (рекомендуется)

```bash
# Запуск бота и Grafana Alloy
docker-compose --profile monitoring up -d

# Проверка логов
docker-compose logs -f grafana-alloy

# UI Alloy доступен по адресу:
# http://localhost:12345
```

### Вариант 2: Только бот (без метрик)

```bash
# Запуск только бота (метрики будут доступны локально)
docker-compose up -d newsagent

# Метрики доступны по адресу:
# http://localhost:8000/metrics
```

## Доступные метрики

Бот экспортирует следующие метрики:

- `telegram_bot_commands_total` - общее количество команд (по типам)
- `telegram_bot_command_duration_seconds` - время выполнения команд
- `telegram_bot_uptime_seconds` - время работы бота
- `telegram_bot_messages_sent_total` - количество отправленных сообщений
- `telegram_bot_errors_total` - количество ошибок (по типам)

## Проверка работы

1. **Проверьте метрики локально**:
```bash
curl http://localhost:8000/metrics
```

2. **Проверьте логи Grafana Alloy**:
```bash
docker-compose logs grafana-alloy
```

3. **Проверьте UI Grafana Alloy**:
   - Откройте http://localhost:12345
   - Проверьте статус компонентов и метрики

4. **Проверьте метрики в Grafana Cloud**:
   - Откройте Grafana Cloud
   - Перейдите в Explore
   - Выполните запрос: `telegram_bot_commands_total`

## Настройка дашборда в Grafana

Создайте дашборд с панелями:

1. **Uptime**: `telegram_bot_uptime_seconds`
2. **Commands per minute**: `rate(telegram_bot_commands_total[1m])`
3. **Command duration**: `histogram_quantile(0.95, telegram_bot_command_duration_seconds_bucket)`
4. **Messages sent**: `telegram_bot_messages_sent_total`
5. **Errors**: `telegram_bot_errors_total`

## Отключение метрик

Если не нужны метрики, просто не запускайте Grafana Alloy:

```bash
docker-compose up -d newsagent
```

Метрики все равно будут собираться локально на порту 8000, но не будут отправляться в Grafana Cloud.

## Конфигурация Alloy

Конфигурация Alloy находится в файле `alloy.config.river` и использует язык River.

Основные компоненты:
- `prometheus.remote_write` - отправка метрик в Grafana Cloud
- `prometheus.scrape` - сбор метрик с бота

Для изменения конфигурации отредактируйте `alloy.config.river` и перезапустите Alloy:
```bash
docker-compose restart grafana-alloy
```

