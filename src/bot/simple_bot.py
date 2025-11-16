"""
Простой Telegram бот для тестирования подключения.
"""
import logging
import time
from typing import Optional
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
try:
    # Для импорта как модуля (из тестов)
    from bot import config
    from bot.metrics import MetricsCollector
except ImportError:
    # Для прямого запуска (из той же директории)
    import config
    from metrics import MetricsCollector

# Глобальная переменная для метрик (инициализируется в main)
metrics: Optional[MetricsCollector] = None

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start."""
    start_time = time.time()
    try:
        await update.message.reply_text(
            f'Привет! Бот работает!\n'
            f'Ваш Chat ID: {update.effective_chat.id}'
        )
        if metrics:
            metrics.record_message_sent()
    except Exception as e:
        logger.error(f"Ошибка в команде /start: {e}")
        if metrics:
            metrics.record_error('command_start')
        raise
    finally:
        duration = time.time() - start_time
        if metrics:
            metrics.record_command('start', duration)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help."""
    start_time = time.time()
    try:
        await update.message.reply_text('Используйте /start для начала работы.')
        if metrics:
            metrics.record_message_sent()
    except Exception as e:
        logger.error(f"Ошибка в команде /help: {e}")
        if metrics:
            metrics.record_error('command_help')
        raise
    finally:
        duration = time.time() - start_time
        if metrics:
            metrics.record_command('help', duration)


async def setup_bot(application: Application) -> None:
    """Настройка бота перед запуском: удаление webhook если установлен."""
    try:
        bot = application.bot
        webhook_info = await bot.get_webhook_info()
        if webhook_info.url:
            logger.info(f"Удаляем существующий webhook: {webhook_info.url}")
            await bot.delete_webhook(drop_pending_updates=True)
            logger.info("✅ Webhook удален, переходим на polling")
    except Exception as e:
        logger.warning(f"Не удалось проверить/удалить webhook: {e}")


def main() -> None:
    """Запуск бота."""
    try:
        # config.py сам проверит наличие токена и выбросит ошибку если его нет
        token = config.TELEGRAM_BOT_TOKEN
    except ValueError as e:
        print(f"❌ ОШИБКА КОНФИГУРАЦИИ:")
        print(f"   {e}")
        print("\n💡 Решение:")
        print("   В Docker: проверьте секцию env_file в docker-compose.yml")
        print("   Локально: экспортируйте переменную: export TELEGRAM_BOT_TOKEN=ваш_токен")
        print("   Получите токен у @BotFather в Telegram")
        return
    
    # Инициализация метрик (Prometheus endpoint для Grafana Agent)
    global metrics
    metrics = MetricsCollector(port=config.METRICS_PORT)
    metrics.start()
    print(f"📊 Prometheus metrics endpoint запущен на порту {config.METRICS_PORT}")
    
    # Создание приложения
    application = Application.builder().token(token).post_init(setup_bot).build()
    
    # Регистрация обработчиков команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    # Запуск бота
    print("🤖 Запуск Telegram бота...")
    print("   Нажмите Ctrl+C для остановки")
    
    try:
        application.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)
    except KeyboardInterrupt:
        logger.info("Получен сигнал остановки...")
    finally:
        if metrics:
            metrics.stop()


if __name__ == '__main__':
    main()

