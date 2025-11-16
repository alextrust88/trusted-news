#!/bin/bash
# Скрипт для запуска тестов и линтера Go парсера в Docker

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARSER_DIR="$SCRIPT_DIR/../src/parser"

echo "🔍 Запуск тестов Go парсера..."
echo ""

cd "$PARSER_DIR"

echo "📋 Тесты:"
docker run --rm -v "$(pwd):/work" -w /work golang:1.21-alpine go test -v ./...

echo ""
echo "🔍 Линтер (go vet):"
docker run --rm -v "$(pwd):/work" -w /work golang:1.21-alpine go vet ./...

echo ""
echo "📐 Проверка форматирования (gofmt):"
if docker run --rm -v "$(pwd):/work" -w /work golang:1.21-alpine sh -c "gofmt -s -l . | wc -l" | grep -q "^0$"; then
    echo "✅ Code is properly formatted"
else
    echo "❌ Code is not formatted. Run: gofmt -s -w ."
    echo ""
    echo "Diff:"
    docker run --rm -v "$(pwd):/work" -w /work golang:1.21-alpine gofmt -s -d .
    exit 1
fi

echo ""
echo "✅ Все проверки пройдены!"

