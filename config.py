"""
Конфигурационный файл.
Читает настройки из переменных окружения или .env файла.
"""
import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла (если он существует)
load_dotenv()

# Токен вашего Telegram бота (получите у @BotFather)
# Устанавливается через переменную окружения TELEGRAM_BOT_TOKEN
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

# ID вашего чата (получите у @userinfobot)
# Устанавливается через переменную окружения TELEGRAM_CHAT_ID
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# Prometheus metrics endpoint (для Grafana Agent)
METRICS_PORT = int(os.getenv("METRICS_PORT", "8000"))

# Проверка наличия обязательных переменных
if not TELEGRAM_BOT_TOKEN:
    raise ValueError(
        "TELEGRAM_BOT_TOKEN не установлен. "
        "Создайте файл .env или установите переменную окружения."
    )

