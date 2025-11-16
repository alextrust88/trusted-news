"""
Модуль для сбора метрик и экспорта через Prometheus endpoint.
Grafana Agent будет скрапить эти метрики и отправлять в Grafana Cloud.
"""
import logging
import time
import threading
from typing import Optional
from prometheus_client import Counter, Histogram, Gauge, start_http_server, REGISTRY

logger = logging.getLogger(__name__)

# Метрики
commands_total = Counter(
    'telegram_bot_commands_total',
    'Total number of commands received',
    ['command']
)

command_duration = Histogram(
    'telegram_bot_command_duration_seconds',
    'Time spent processing commands',
    ['command']
)

bot_uptime = Gauge(
    'telegram_bot_uptime_seconds',
    'Bot uptime in seconds'
)

messages_sent = Counter(
    'telegram_bot_messages_sent_total',
    'Total number of messages sent'
)

errors_total = Counter(
    'telegram_bot_errors_total',
    'Total number of errors',
    ['error_type']
)


class MetricsCollector:
    """Класс для сбора и экспорта метрик через Prometheus endpoint."""
    
    def __init__(self, port: int = 8000) -> None:
        """
        Инициализация сбора метрик.
        
        Args:
            port: Порт для Prometheus metrics endpoint
        """
        self.port = port
        self.start_time = time.time()
        self.running = False
        self.thread: Optional[threading.Thread] = None
    
    def start(self) -> None:
        """Запуск HTTP сервера для экспорта метрик."""
        if self.running:
            return
        
        try:
            start_http_server(self.port, registry=REGISTRY)
            self.running = True
            self.thread = threading.Thread(target=self._update_uptime_loop, daemon=True)
            self.thread.start()
            logger.info(f"📊 Prometheus metrics endpoint запущен на порту {self.port}")
            logger.info(f"   Метрики доступны по адресу: http://localhost:{self.port}/metrics")
        except Exception as e:
            logger.error(f"Ошибка при запуске metrics endpoint: {e}")
            errors_total.labels(error_type='metrics_start').inc()
    
    def stop(self) -> None:
        """Остановка обновления метрик."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        logger.info("Метрики остановлены")
    
    def _update_uptime_loop(self) -> None:
        """Цикл обновления метрики uptime."""
        while self.running:
            try:
                uptime = time.time() - self.start_time
                bot_uptime.set(uptime)
                time.sleep(10)  # Обновляем каждые 10 секунд
            except Exception as e:
                logger.error(f"Ошибка при обновлении uptime: {e}")
                time.sleep(10)
    
    def record_command(self, command: str, duration: float) -> None:
        """Запись метрики команды."""
        commands_total.labels(command=command).inc()
        command_duration.labels(command=command).observe(duration)
    
    def record_message_sent(self) -> None:
        """Запись отправки сообщения."""
        messages_sent.inc()
    
    def record_error(self, error_type: str) -> None:
        """Запись ошибки."""
        errors_total.labels(error_type=error_type).inc()

