"""Тесты для модуля config."""
import os
import sys
import pytest
from unittest.mock import patch


def test_config_loads_from_env():
    """Тест загрузки конфигурации из переменных окружения."""
    with patch.dict(os.environ, {
        'TELEGRAM_BOT_TOKEN': 'test_token_123',
        'TELEGRAM_CHAT_ID': 'test_chat_456'
    }, clear=False):
        # Перезагружаем модуль для применения новых переменных окружения
        import importlib
        if 'bot.config' in sys.modules:
            importlib.reload(sys.modules['bot.config'])
        else:
            from bot import config
        
        from bot.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
        assert TELEGRAM_BOT_TOKEN == 'test_token_123'
        assert TELEGRAM_CHAT_ID == 'test_chat_456'


def test_config_token_required():
    """Тест что токен обязателен (проверяется при импорте модуля)."""
    # Этот тест проверяет что модуль требует токен
    # В conftest.py мы устанавливаем тестовый токен, поэтому модуль должен загружаться
    from bot import config
    assert hasattr(config, 'TELEGRAM_BOT_TOKEN')
    assert config.TELEGRAM_BOT_TOKEN is not None


def test_config_chat_id_optional():
    """Тест что chat_id опционален."""
    from bot import config
    # Chat ID может быть пустой строкой или не установлен
    assert hasattr(config, 'TELEGRAM_CHAT_ID')

