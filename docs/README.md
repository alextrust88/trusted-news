# NewsAgent

Модульная система для сбора и отправки новостей через Telegram бота.

## Структура проекта

```
NewsAgent/
├── bot/              # Telegram бот модуль
│   ├── __init__.py
│   ├── simple_bot.py
│   ├── metrics.py
│   ├── config.py
│   └── Dockerfile
├── database/         # Модуль базы данных
│   └── __init__.py
├── parser/           # Модуль парсера новостей
│   └── __init__.py
├── docker/           # Docker конфигурации
│   ├── docker-compose.yml
│   ├── docker-compose.prod.yml
│   └── alloy.config.river
├── tests/            # Тесты
│   ├── bot/
│   ├── database/
│   └── parser/
└── README.md
```

## Модули

### 1. Bot (`bot/`)
Telegram бот для отправки новостей пользователям.

**Файлы:**
- `simple_bot.py` - основной файл бота
- `metrics.py` - сбор метрик Prometheus
- `config.py` - конфигурация
- `Dockerfile` - образ для бота

### 2. Database (`database/`)
Модуль для работы с базой данных (будет добавлен).

### 3. Parser (`parser/`)
Модуль для парсинга новостей из различных источников (будет добавлен).

## Быстрый старт

См. [SETUP.md](SETUP.md) для инструкций по установке и запуску.

## Деплой

См. [DEPLOY.md](DEPLOY.md) для инструкций по деплою на сервер.

## Документация

- [SETUP.md](SETUP.md) - Установка и настройка
- [DEPLOY.md](DEPLOY.md) - Деплой на сервер
- [DOCKER.md](DOCKER.md) - Работа с Docker
- [CHECK_METRICS.md](CHECK_METRICS.md) - Проверка метрик
- [GRAFANA.md](GRAFANA.md) - Настройка Grafana
