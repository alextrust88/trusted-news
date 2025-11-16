# Многостадийная сборка для Go приложения
FROM golang:1.21-alpine AS builder

# Устанавливаем рабочую директорию
WORKDIR /build

# Копируем go.mod и go.sum (если есть) для кеширования зависимостей
# Context будет корень проекта, поэтому путь src/parser/go.mod
COPY src/parser/go.mod src/parser/go.sum* ./
RUN go mod download

# Копируем исходный код парсера
COPY src/parser/*.go ./

# Собираем приложение
# CGO_ENABLED=0 для статической сборки
# -ldflags="-w -s" для уменьшения размера бинарника
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -ldflags="-w -s" -o parser .

# Финальный образ
FROM alpine:latest

# Устанавливаем ca-certificates для HTTPS запросов
RUN apk --no-cache add ca-certificates

WORKDIR /app

# Копируем бинарник из builder
COPY --from=builder /build/parser .

# Запускаем парсер
CMD ["./parser"]

