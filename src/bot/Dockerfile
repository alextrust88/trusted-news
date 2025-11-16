# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей (для кеширования слоев)
COPY src/bot/pyproject.toml src/bot/uv.lock ./

# Устанавливаем зависимости через uv (кешируется если pyproject.toml не изменился)
RUN uv sync --frozen

# Копируем код приложения бота
COPY src/bot/ ./bot/

# Запускаем бота
WORKDIR /app/bot
CMD ["uv", "run", "python", "simple_bot.py"]

