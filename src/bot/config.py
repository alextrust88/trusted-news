"""
Конфигурационный файл.
Читает настройки из переменных окружения.
В Docker контейнере переменные передаются через env_file в docker-compose.yml.
"""
import os

# Токен вашего Telegram бота (получите у @BotFather)
# Обязательная переменная окружения: TELEGRAM_BOT_TOKEN
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

# ID вашего чата (получите у @userinfobot)
# Опциональная переменная окружения: TELEGRAM_CHAT_ID
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# Prometheus metrics endpoint (для Grafana Agent)
# По умолчанию: 8000
METRICS_PORT = int(os.getenv("METRICS_PORT", "8000"))

# Проверка наличия обязательных переменных
if not TELEGRAM_BOT_TOKEN:
    raise ValueError(
        "TELEGRAM_BOT_TOKEN не установлен.\n"
        "Установите переменную окружения TELEGRAM_BOT_TOKEN.\n"
        "В Docker: добавьте в docker-compose.yml секцию env_file или environment.\n"
        "Локально: экспортируйте переменную: export TELEGRAM_BOT_TOKEN=ваш_токен"
    )

