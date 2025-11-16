# Структура проекта NewsAgent

## Обзор

Проект организован в модульную структуру для разделения функциональности на отдельные компоненты. Проект использует **мультиязычный подход**: бот на Python, парсер на Go.

```
NewsAgent/
├── src/                    # Исходный код
│   ├── bot/                # Модуль Telegram бота (Python)
│   │   ├── __init__.py
│   │   ├── simple_bot.py   # Основной файл бота
│   │   ├── metrics.py      # Сбор метрик Prometheus
│   │   ├── config.py        # Конфигурация
│   │   ├── pyproject.toml  # Python зависимости
│   │   ├── uv.lock         # Зафиксированные версии
│   │   ├── pytest.ini      # Конфигурация pytest для модуля
│   │   ├── Dockerfile      # Docker образ для бота
│   │   └── tests/          # Тесты для бота
│   │       ├── __init__.py
│   │       ├── conftest.py
│   │       ├── test_config.py
│   │       └── test_simple_bot.py
│   │
│   ├── parser/             # Модуль парсера новостей (Go)
│   │   ├── go.mod          # Go модуль
│   │   ├── main.go         # Точка входа
│   │   ├── main_test.go    # Тесты для парсера
│   │   ├── Dockerfile      # Docker образ для парсера
│   │   └── ...             # Go исходники
│   │
│   ├── database/           # Модуль базы данных
│   │   ├── __init__.py
│   │   ├── pytest.ini      # Конфигурация pytest для модуля
│   │   └── tests/          # Тесты для database
│   │       └── __init__.py
│   │
│   └── agents/             # Агенты для различных задач
│       ├── .gitkeep
│       ├── pytest.ini      # Конфигурация pytest для модуля
│       └── tests/          # Тесты для agents
│           └── __init__.py
│
├── docker/                 # Docker конфигурации
│   ├── docker-compose.yml          # Для разработки
│   └── docker-compose.prod.yml     # Для продакшена
│
├── configs/                # Конфигурационные файлы
│   └── alloy.config.river   # Конфигурация Grafana Alloy
│
├── scripts/                # Диагностические утилиты
│   ├── diagnose_metrics.sh
│   └── README.md
│
├── docs/                   # Документация
│   ├── SETUP.md
│   ├── DEPLOY.md
│   ├── DOCKER.md
│   ├── CHECK_METRICS.md
│   ├── GRAFANA.md
│   └── ...
│
├── tests/                    # Общие тесты (если нужны)
│   └── __init__.py
│
├── README.md                # Основной README
└── docs/                    # Документация
    └── README.md            # Документация модулей
```

## Модули

### Bot (`src/bot/`) - Python
Telegram бот для отправки новостей пользователям.

**Технологии:** Python 3.11, python-telegram-bot, Prometheus

**Основные файлы:**
- `simple_bot.py` - основной файл бота с обработчиками команд
- `metrics.py` - сбор и экспорт метрик Prometheus
- `config.py` - загрузка конфигурации из переменных окружения
- `Dockerfile` - образ для запуска бота в Docker

**Зависимости:**
- `python-telegram-bot` - библиотека для работы с Telegram Bot API
- `prometheus-client` - сбор метрик
- `python-dotenv` - загрузка переменных окружения

**Управление зависимостями:**
```bash
# Переход в директорию бота
cd src/bot

# Установка
uv sync

# Запуск
uv run python simple_bot.py
```

### Parser (`src/parser/`) - Go
Модуль для парсинга новостей из различных источников.

**Технологии:** Go 1.21+

**Основные файлы:**
- `main.go` - точка входа приложения
- `go.mod` - Go модуль и зависимости
- `Dockerfile` - образ для запуска парсера в Docker

**Планируется для:**
- Парсинга RSS лент
- Парсинга веб-сайтов
- Агрегации новостей из разных источников
- Отправки данных в базу данных или боту

**Управление зависимостями:**
```bash
# Установка зависимостей
cd src/parser
go mod download

# Запуск
go run main.go

# Сборка
go build -o parser main.go
```

### Database (`src/database/`)
Модуль для работы с базой данных (будет добавлен).

Планируется для:
- Хранения истории новостей
- Кеширования парсированных данных
- Хранения пользовательских настроек

### Agents (`src/agents/`)
Агенты для различных задач (будет добавлен).

## Docker

### Разработка
Используйте `docker/docker-compose.yml` для локальной разработки:
```bash
cd docker
docker compose up
```

### Продакшен
Используйте `docker/docker-compose.prod.yml` для деплоя:
```bash
cd docker
docker compose -f docker-compose.prod.yml up -d
```

**Образы:**
- `ghcr.io/alextrust88/trusted-news:latest` - бот (Python)
- `ghcr.io/alextrust88/trusted-news-parser:latest` - парсер (Go)

## Тесты

Тесты организованы по модулям и находятся рядом с кодом:
- `src/bot/tests/` - тесты для бота (Python, pytest)
- `src/parser/*_test.go` - тесты для парсера (Go, go test)
- `src/database/tests/` - тесты для БД (будет добавлено)
- `src/agents/tests/` - тесты для агентов (будет добавлено)

**Запуск тестов:**
```bash
# Python тесты (бот)
cd src/bot
uv run pytest

# Python тесты (database)
cd src/database
uv run pytest

# Python тесты (agents)
cd src/agents
uv run pytest

# Go тесты (парсер)
cd src/parser
go test ./...
```

**Примечание:** Каждый Python модуль имеет свой `pytest.ini` в своей директории, что позволяет независимо настраивать тесты для каждого модуля.

## CI/CD

GitHub Actions автоматически:
1. Запускает тесты для Python (бот) и Go (парсер)
2. Собирает Docker образы для обоих модулей
3. Публикует образы в GitHub Container Registry
4. Деплоит на сервер

## Добавление нового модуля

### Python модуль:
1. Создайте директорию: `mkdir src/new_module`
2. Создайте `__init__.py`: `touch src/new_module/__init__.py`
3. Добавьте код модуля
4. Добавьте зависимости в `pyproject.toml`
5. Добавьте тесты в `tests/new_module/`

### Go модуль:
1. Создайте директорию: `mkdir src/new_module`
2. Инициализируйте Go модуль: `cd src/new_module && go mod init github.com/alextrust88/trusted-news/new_module`
3. Добавьте код модуля
4. Добавьте тесты в `src/new_module/` с суффиксом `_test.go`
5. Создайте `Dockerfile` для сборки образа
