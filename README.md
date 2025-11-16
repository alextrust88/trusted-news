# NewsAgent

Модульная система для сбора и отправки новостей через Telegram бота.

## Структура проекта

```
NewsAgent/
├── src/              # Исходный код
│   ├── bot/          # Telegram бот (Python)
│   ├── parser/        # Парсер новостей (Go)
│   ├── database/     # База данных
│   └── agents/        # Агенты
├── docker/           # Docker конфигурации
├── configs/          # Конфигурационные файлы
├── scripts/          # Диагностические утилиты
├── docs/             # Документация
└── README.md         # Этот файл
```

## Быстрый старт

См. [docs/SETUP.md](docs/SETUP.md) для инструкций по установке и запуску.

## Документация

Вся документация находится в папке [`docs/`](docs/):

- [docs/SETUP.md](docs/SETUP.md) - Установка и настройка
- [docs/DEPLOY.md](docs/DEPLOY.md) - Деплой на сервер
- [docs/DEPLOY_TROUBLESHOOTING.md](docs/DEPLOY_TROUBLESHOOTING.md) - Решение проблем при деплое
- [docs/DOCKER.md](docs/DOCKER.md) - Работа с Docker
- [docs/CHECK_METRICS.md](docs/CHECK_METRICS.md) - Проверка метрик
- [docs/CHECK_METRICS_COMMANDS.md](docs/CHECK_METRICS_COMMANDS.md) - Команды для проверки метрик
- [docs/GRAFANA.md](docs/GRAFANA.md) - Настройка Grafana
- [docs/SSH_SETUP.md](docs/SSH_SETUP.md) - Настройка SSH для деплоя
- [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md) - Структура проекта

## Модули

### Bot (`src/bot/`) - Python
Telegram бот для отправки новостей пользователям.

**Технологии:** Python 3.11, python-telegram-bot, Prometheus

### Parser (`src/parser/`) - Go
Модуль для парсинга новостей из различных источников.

**Технологии:** Go 1.21+

**Запуск:**
```bash
cd src/parser
go run main.go
```

### Database (`src/database/`)
Модуль для работы с базой данных (будет добавлен).

### Agents (`src/agents/`)
Агенты для различных задач (будет добавлен).

## Разработка

### Python (Bot)

```bash
# Переход в директорию бота
cd src/bot

# Установка зависимостей
uv sync

# Запуск тестов (использует локальный pytest.ini)
uv run pytest

# Запуск бота локально
uv run python simple_bot.py
```

### Python (Database)

```bash
# Переход в директорию database
cd src/database

# Установка зависимостей (если есть pyproject.toml)
uv sync

# Запуск тестов (использует локальный pytest.ini)
uv run pytest
```

### Python (Agents)

```bash
# Переход в директорию agents
cd src/agents

# Установка зависимостей (если есть pyproject.toml)
uv sync

# Запуск тестов (использует локальный pytest.ini)
uv run pytest
```

### Go (Parser)

```bash
# Переход в директорию парсера
cd src/parser

# Установка зависимостей
go mod download

# Запуск тестов
go test ./...

# Запуск парсера локально
go run main.go

# Сборка
go build -o parser main.go
```

## Docker

### Локальная разработка

```bash
# Перейдите в директорию docker
cd docker

# Запуск всех сервисов (бот + парсер)
docker compose up -d

# С Grafana Alloy для мониторинга
docker compose --profile monitoring up -d

# Просмотр логов
docker compose logs -f

# Остановка
docker compose down
```

**Сервисы:**
- `newsagent` - Telegram бот (порт 8000 для метрик)
- `parser` - Парсер новостей
- `grafana-alloy` - Сбор метрик (только с профилем `monitoring`, порт 12345)

Подробнее см. [docs/DOCKER.md](docs/DOCKER.md)

## Деплой

См. [docs/DEPLOY.md](docs/DEPLOY.md) для инструкций по деплою на сервер.

