"""Конфигурация pytest для всех тестов."""
import os
import sys
from pathlib import Path

# Добавляем корневую директорию проекта и src в путь
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

# Устанавливаем тестовые переменные окружения по умолчанию
os.environ.setdefault('TELEGRAM_BOT_TOKEN', 'test_token_for_testing')
os.environ.setdefault('TELEGRAM_CHAT_ID', 'test_chat_id_for_testing')

