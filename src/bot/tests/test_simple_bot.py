"""Тесты для модуля simple_bot."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from telegram.ext import ContextTypes


@pytest.fixture
def mock_update():
    """Создает полностью мокированный Update для тестов."""
    # Используем MagicMock так как реальные объекты Telegram frozen
    update = MagicMock()
    update.message = MagicMock()
    update.message.reply_text = AsyncMock()
    update.effective_chat = MagicMock()
    update.effective_chat.id = 123456
    return update


@pytest.fixture
def mock_context():
    """Создает мок объект Context для тестов."""
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
    return context


@pytest.mark.asyncio
async def test_start_command(mock_update, mock_context):
    """Тест команды /start."""
    from bot.simple_bot import start
    
    await start(mock_update, mock_context)
    
    # Проверяем что reply_text был вызван
    assert mock_update.message.reply_text.called
    call_args = mock_update.message.reply_text.call_args[0][0]
    assert 'Привет' in call_args
    assert '123456' in str(call_args)  # Chat ID


@pytest.mark.asyncio
async def test_help_command(mock_update, mock_context):
    """Тест команды /help."""
    from bot.simple_bot import help_command
    
    await help_command(mock_update, mock_context)
    
    # Проверяем что reply_text был вызван
    assert mock_update.message.reply_text.called
    call_args = mock_update.message.reply_text.call_args[0][0]
    assert 'start' in call_args.lower()


def test_main_without_token():
    """Тест что main выводит ошибку при отсутствии токена."""
    # Мокаем config чтобы он выбрасывал ValueError при доступе к TELEGRAM_BOT_TOKEN
    with patch('bot.simple_bot.config') as mock_config:
        # Создаем PropertyMock для симуляции ошибки при доступе
        type(mock_config).TELEGRAM_BOT_TOKEN = property(
            lambda self: (_ for _ in ()).throw(ValueError("TELEGRAM_BOT_TOKEN не установлен"))
        )
        
        with patch('builtins.print') as mock_print:
            from bot.simple_bot import main
            main()
            
            # Проверяем что была выведена ошибка
            assert mock_print.called
            print_calls = str(mock_print.call_args_list)
            assert 'ОШИБКА' in print_calls or 'TELEGRAM_BOT_TOKEN' in print_calls


def test_main_with_token():
    """Тест что main создает приложение при наличии токена."""
    with patch('bot.simple_bot.config') as mock_config:
        mock_config.TELEGRAM_BOT_TOKEN = 'test_token'
        mock_config.METRICS_PORT = 8000
        
        with patch('bot.simple_bot.MetricsCollector') as mock_metrics_class:
            mock_metrics = MagicMock()
            mock_metrics_class.return_value = mock_metrics
            
            with patch('bot.simple_bot.Application') as mock_app_class:
                mock_app = MagicMock()
                mock_builder = MagicMock()
                mock_builder.token.return_value = mock_builder
                mock_builder.post_init.return_value = mock_builder
                mock_builder.build.return_value = mock_app
                mock_app_class.builder.return_value = mock_builder
                
                with patch('builtins.print'):
                    from bot.simple_bot import main
                    main()
                    
                    # Проверяем что Application был создан
                    assert mock_app_class.builder.called
                    assert mock_app.add_handler.called

