#!/bin/bash
# Скрипт для диагностики метрик на сервере

echo "🔍 Диагностика метрик NewsAgent"
echo "================================"
echo ""

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Определяем команду docker compose
if docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
    echo "✅ Используем: docker compose (новый синтаксис)"
elif command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
    echo "✅ Используем: docker-compose (старый синтаксис)"
else
    echo -e "${RED}❌ docker compose не найден${NC}"
    echo "Установите Docker Compose:"
    echo "  sudo apt-get install docker-compose-plugin  # новый синтаксис"
    echo "  или"
    echo "  sudo apt-get install docker-compose         # старый синтаксис"
    exit 1
fi
echo ""

# Проверка 1: Статус контейнера
echo "1️⃣  Проверка статуса контейнера..."
if docker ps | grep -q newsagent-bot; then
    echo -e "${GREEN}✅ Контейнер запущен${NC}"
    docker ps | grep newsagent-bot
else
    echo -e "${RED}❌ Контейнер не запущен${NC}"
    echo "Попробуйте: $COMPOSE_CMD -f docker-compose.prod.yml ps"
    exit 1
fi
echo ""

# Проверка 2: Логи контейнера
echo "2️⃣  Последние логи контейнера (последние 30 строк)..."
echo "---"
docker logs --tail=30 newsagent-bot 2>&1
echo "---"
echo ""

# Проверка 3: Проверка порта
echo "3️⃣  Проверка порта 8000..."
if netstat -tlnp 2>/dev/null | grep -q ":8000" || ss -tlnp 2>/dev/null | grep -q ":8000"; then
    echo -e "${GREEN}✅ Порт 8000 слушается${NC}"
    netstat -tlnp 2>/dev/null | grep ":8000" || ss -tlnp 2>/dev/null | grep ":8000"
else
    echo -e "${RED}❌ Порт 8000 не слушается${NC}"
fi
echo ""

# Проверка 4: Доступность метрик из контейнера
echo "4️⃣  Проверка метрик изнутри контейнера..."
METRICS_RESPONSE=$(docker exec newsagent-bot curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/metrics 2>/dev/null || echo "000")
if [ "$METRICS_RESPONSE" = "200" ]; then
    echo -e "${GREEN}✅ Метрики доступны изнутри контейнера (HTTP $METRICS_RESPONSE)${NC}"
    echo "Первые 10 строк метрик:"
    docker exec newsagent-bot curl -s http://localhost:8000/metrics 2>/dev/null | head -10
else
    echo -e "${RED}❌ Метрики недоступны изнутри контейнера (HTTP $METRICS_RESPONSE)${NC}"
fi
echo ""

# Проверка 5: Доступность метрик с хоста
echo "5️⃣  Проверка метрик с хоста (localhost:8000)..."
HOST_METRICS_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 http://localhost:8000/metrics 2>/dev/null || echo "000")
if [ "$HOST_METRICS_RESPONSE" = "200" ]; then
    echo -e "${GREEN}✅ Метрики доступны с хоста (HTTP $HOST_METRICS_RESPONSE)${NC}"
    echo "Первые 10 строк метрик:"
    curl -s http://localhost:8000/metrics 2>/dev/null | head -10
else
    echo -e "${RED}❌ Метрики недоступны с хоста (HTTP $HOST_METRICS_RESPONSE)${NC}"
    echo "Возможные причины:"
    echo "  - Порт не проброшен в docker-compose.prod.yml"
    echo "  - Firewall блокирует порт"
    echo "  - Приложение не запустилось внутри контейнера"
fi
echo ""

# Проверка 6: Переменные окружения
echo "6️⃣  Проверка переменных окружения..."
if [ -f .env ]; then
    echo -e "${GREEN}✅ Файл .env существует${NC}"
    echo "Проверка наличия обязательных переменных:"
    if grep -q "TELEGRAM_BOT_TOKEN" .env && ! grep -q "^TELEGRAM_BOT_TOKEN=$" .env; then
        echo -e "${GREEN}  ✅ TELEGRAM_BOT_TOKEN установлен${NC}"
    else
        echo -e "${RED}  ❌ TELEGRAM_BOT_TOKEN не установлен или пуст${NC}"
    fi
    if grep -q "TELEGRAM_CHAT_ID" .env && ! grep -q "^TELEGRAM_CHAT_ID=$" .env; then
        echo -e "${GREEN}  ✅ TELEGRAM_CHAT_ID установлен${NC}"
    else
        echo -e "${RED}  ❌ TELEGRAM_CHAT_ID не установлен или пуст${NC}"
    fi
    if grep -q "METRICS_PORT" .env; then
        METRICS_PORT=$(grep "^METRICS_PORT=" .env | cut -d'=' -f2)
        echo -e "${GREEN}  ✅ METRICS_PORT=$METRICS_PORT${NC}"
    else
        echo -e "${YELLOW}  ⚠️  METRICS_PORT не установлен (будет использован 8000)${NC}"
    fi
else
    echo -e "${RED}❌ Файл .env не найден${NC}"
fi
echo ""

# Проверка 7: Процессы внутри контейнера
echo "7️⃣  Процессы внутри контейнера..."
docker exec newsagent-bot ps aux 2>/dev/null | head -10
echo ""

# Проверка 8: Проверка сетевых подключений контейнера
echo "8️⃣  Сетевые подключения контейнера..."
docker exec newsagent-bot netstat -tlnp 2>/dev/null | grep -E "8000|LISTEN" || \
docker exec newsagent-bot ss -tlnp 2>/dev/null | grep -E "8000|LISTEN" || \
echo "Не удалось проверить сетевые подключения"
echo ""

# Проверка 9: Конфигурация docker-compose
echo "9️⃣  Проверка конфигурации docker-compose..."
if [ -f docker-compose.prod.yml ]; then
    echo "Проверка проброса порта 8000:"
    if grep -A 5 "ports:" docker-compose.prod.yml | grep -q "8000"; then
        echo -e "${GREEN}✅ Порт 8000 проброшен${NC}"
        grep -A 5 "ports:" docker-compose.prod.yml | grep "8000"
    else
        echo -e "${RED}❌ Порт 8000 не проброшен${NC}"
    fi
    echo ""
    echo "Статус через docker compose:"
    $COMPOSE_CMD -f docker-compose.prod.yml ps
else
    echo -e "${RED}❌ Файл docker-compose.prod.yml не найден${NC}"
fi
echo ""

# Итоговая рекомендация
echo "📋 Итоговая диагностика:"
echo "================================"
if [ "$METRICS_RESPONSE" = "200" ] && [ "$HOST_METRICS_RESPONSE" = "200" ]; then
    echo -e "${GREEN}✅ Метрики работают корректно!${NC}"
    echo ""
    echo "Проверьте доступность извне:"
    echo "  curl http://$(hostname -I | awk '{print $1}'):8000/metrics"
elif [ "$METRICS_RESPONSE" = "200" ] && [ "$HOST_METRICS_RESPONSE" != "200" ]; then
    echo -e "${YELLOW}⚠️  Метрики работают внутри контейнера, но недоступны с хоста${NC}"
    echo ""
    echo "Возможные решения:"
    echo "  1. Проверьте проброс порта в docker-compose.prod.yml"
    echo "  2. Проверьте firewall: sudo ufw status"
    echo "  3. Проверьте что порт слушается: netstat -tlnp | grep 8000"
elif [ "$METRICS_RESPONSE" != "200" ]; then
    echo -e "${RED}❌ Метрики не работают внутри контейнера${NC}"
    echo ""
    echo "Возможные решения:"
    echo "  1. Проверьте логи: docker logs newsagent-bot"
    echo "  2. Проверьте переменные окружения в .env"
    echo "  3. Проверьте что приложение запустилось: docker exec newsagent-bot ps aux"
    echo "  4. Перезапустите контейнер: docker-compose -f docker-compose.prod.yml restart newsagent"
fi
echo ""

