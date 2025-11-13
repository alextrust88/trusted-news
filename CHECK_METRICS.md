# Как проверить метрики

## 1. Локальная проверка метрик бота

### Через curl (командная строка)

```bash
# Все метрики
curl http://localhost:8000/metrics

# Только метрики бота
curl http://localhost:8000/metrics | grep telegram_bot

# Конкретная метрика
curl http://localhost:8000/metrics | grep telegram_bot_commands_total
```

### Через браузер

Откройте в браузере: http://localhost:8000/metrics

## 2. Проверка через Grafana Alloy UI

Если запущен Grafana Alloy:

```bash
# Откройте в браузере
http://localhost:12345
```

В UI Alloy вы увидите:
- Статус компонентов
- Метрики, которые собираются
- Логи работы

## 3. Проверка в Grafana Cloud

1. Откройте Grafana Cloud
2. Перейдите в **Explore**
3. Выполните запросы:

```promql
# Общее количество команд
telegram_bot_commands_total

# Команды по типам
telegram_bot_commands_total{command="start"}
telegram_bot_commands_total{command="help"}

# Время работы бота
telegram_bot_uptime_seconds

# Количество отправленных сообщений
telegram_bot_messages_sent_total

# Количество ошибок
telegram_bot_errors_total

# Скорость выполнения команд (команд в минуту)
rate(telegram_bot_commands_total[1m])

# Среднее время выполнения команды
rate(telegram_bot_command_duration_seconds_sum[5m]) / rate(telegram_bot_command_duration_seconds_count[5m])
```

## 4. Доступные метрики

### Счетчики (Counters)

- `telegram_bot_commands_total{command}` - общее количество команд (по типам)
- `telegram_bot_messages_sent_total` - общее количество отправленных сообщений
- `telegram_bot_errors_total{error_type}` - общее количество ошибок (по типам)

### Гистограммы (Histograms)

- `telegram_bot_command_duration_seconds{command}` - время выполнения команд
  - `_bucket` - buckets для квантилей
  - `_sum` - сумма времени
  - `_count` - количество измерений

### Gauges

- `telegram_bot_uptime_seconds` - время работы бота в секундах

## 5. Тестирование метрик

Чтобы метрики появились, нужно:

1. **Отправить команду боту** в Telegram:
   - `/start` - увеличит `telegram_bot_commands_total{command="start"}`
   - `/help` - увеличит `telegram_bot_commands_total{command="help"}`

2. **Проверить метрики**:
```bash
curl http://localhost:8000/metrics | grep telegram_bot_commands_total
```

## 6. Проверка работы Grafana Alloy

```bash
# Логи Alloy
docker-compose logs grafana-alloy

# Проверка что Alloy скрапит метрики
docker-compose exec grafana-alloy wget -qO- http://newsagent:8000/metrics | head -5
```

## 7. Полезные запросы для Grafana

### Дашборд метрик

```promql
# Uptime в часах
telegram_bot_uptime_seconds / 3600

# Команды в минуту
rate(telegram_bot_commands_total[1m]) * 60

# 95-й перцентиль времени выполнения команды
histogram_quantile(0.95, rate(telegram_bot_command_duration_seconds_bucket[5m]))

# Сообщений в минуту
rate(telegram_bot_messages_sent_total[1m]) * 60

# Ошибок в минуту
rate(telegram_bot_errors_total[1m]) * 60
```

## 8. Отладка

Если метрики не появляются:

1. Проверьте что бот запущен:
```bash
docker-compose ps
docker-compose logs newsagent
```

2. Проверьте что порт 8000 доступен:
```bash
curl http://localhost:8000/metrics
```

3. Проверьте что Alloy запущен (если используется):
```bash
docker-compose ps grafana-alloy
docker-compose logs grafana-alloy
```

4. Проверьте конфигурацию Alloy:
```bash
docker-compose exec grafana-alloy cat /etc/alloy/config.river
```

