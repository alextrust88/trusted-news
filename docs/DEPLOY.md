# Инструкция по настройке CI/CD деплоя

## Обзор

Проект настроен для автоматической сборки Docker образа и деплоя на сервер через GitHub Actions.

## Workflows

### 1. `docker-build.yml` - Сборка и публикация образа

**Триггеры:**
- Push в ветку `main`
- Создание тега `v*` (например, `v1.0.0`)
- Pull Request в `main` (только сборка, без публикации)

**Что делает:**
- Собирает Docker образ
- Публикует в GitHub Container Registry (ghcr.io)
- Использует кеширование для ускорения сборки

**Результат:**
Образ доступен по адресу: `ghcr.io/alextrust88/trusted-news:latest`

### 2. `deploy.yml` - Деплой на сервер

**Триггеры:**
- Push в ветку `main` (автоматический деплой)
- Ручной запуск через `workflow_dispatch`

**Что делает:**
- Подключается к серверу по SSH
- Останавливает старые контейнеры
- Обновляет образ из GitHub Container Registry
- Запускает новые контейнеры
- Выполняет health check

## Настройка секретов в GitHub

Перейдите в Settings → Secrets and variables → Actions и добавьте:

### Обязательные секреты:

1. **`DEPLOY_HOST`** - IP адрес или домен сервера
   ```
   example: 192.168.1.100 или server.example.com
   ```

2. **`DEPLOY_USER`** - Пользователь для SSH подключения
   ```
   example: root или deploy
   ```

3. **`DEPLOY_SSH_KEY`** - Приватный SSH ключ для доступа к серверу
   ```
   Полный приватный ключ (включая -----BEGIN OPENSSH PRIVATE KEY-----)
   ```

### Опциональные секреты:

4. **`DEPLOY_PORT`** - SSH порт (по умолчанию 22)
   ```
   example: 2222
   ```

5. **`DEPLOY_PATH`** - Путь к проекту на сервере (по умолчанию `/opt/newsagent`)
   ```
   example: /opt/newsagent или /home/deploy/newsagent
   ```

## Подготовка сервера

### 1. Установите Docker и Docker Compose

```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Установите Docker Compose plugin (новый способ)
sudo apt-get update
sudo apt-get install docker-compose-plugin

# Или установите старый docker-compose (если нужен)
sudo apt-get install docker-compose

# Добавьте пользователя в группу docker (чтобы не использовать sudo)
sudo usermod -aG docker $USER
# Выйдите и войдите заново или выполните:
newgrp docker

# Проверка
docker --version
docker compose version  # новый синтаксис
# или
docker-compose --version  # старый синтаксис
```

**Важно:** 
- Убедитесь что Docker доступен без sudo для пользователя деплоя!
- Проверьте что команды `docker` и `docker compose` (или `docker-compose`) работают без sudo

### 2. Создайте директорию проекта

```bash
sudo mkdir -p /opt/newsagent
sudo chown $USER:$USER /opt/newsagent
cd /opt/newsagent
```

### 3. Склонируйте репозиторий (или создайте структуру)

```bash
git clone https://github.com/alextrust88/trusted-news.git /opt/newsagent
# или
mkdir -p /opt/newsagent
cd /opt/newsagent
```

### 4. Создайте файл `.env` на сервере

**⚠️ ВАЖНО:** Файл `.env` должен быть создан на сервере до первого деплоя!

```bash
cd /opt/newsagent
nano .env
```

Добавьте следующие переменные (обязательные для работы бота):
```bash
TELEGRAM_BOT_TOKEN=ваш_токен_от_@BotFather
TELEGRAM_CHAT_ID=ваш_chat_id
METRICS_PORT=8000
```

Если используете Grafana Cloud для мониторинга, добавьте также:
```bash
GCLOUD_HOSTED_METRICS_URL=https://prometheus-prod-01-eu-west-0.grafana.net/api/prom/push
GCLOUD_HOSTED_METRICS_ID=ваш_metrics_id
GCLOUD_RW_API_KEY=ваш_api_ключ
```

**Проверка прав доступа:**
```bash
chmod 600 .env  # Только владелец может читать
ls -la .env     # Должен показать права -rw------- 
```

### 5. Скопируйте необходимые файлы

```bash
cd /opt/newsagent
# Скопируйте из репозитория:
# - docker-compose.prod.yml
# - alloy.config.river
```

### 6. Настройте SSH доступ

#### Шаг 1: Создайте SSH ключ (если еще нет)

```bash
# На вашем локальном компьютере создайте SSH ключ
ssh-keygen -t ed25519 -C "github-actions-deploy"

# Или используйте существующий ключ
# Проверьте существующие ключи:
ls -la ~/.ssh/
```

#### Шаг 2: Скопируйте публичный ключ на сервер

```bash
# Скопируйте публичный ключ на сервер
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@server

# Или вручную:
cat ~/.ssh/id_ed25519.pub | ssh user@server "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

#### Шаг 3: Добавьте приватный ключ в GitHub Secrets

1. **Скопируйте приватный ключ:**
```bash
# Покажите приватный ключ (скопируйте ВСЁ содержимое)
cat ~/.ssh/id_ed25519
```

2. **Добавьте в GitHub Secrets (Settings → Secrets and variables → Actions):**

   Перейдите в ваш репозиторий на GitHub → Settings → Secrets and variables → Actions
   
   Добавьте следующие секреты:
   
   - **`DEPLOY_HOST`** - IP адрес или домен сервера
   - **`DEPLOY_USER`** - имя пользователя для SSH (например, `deploy` или `root`)
   - **`DEPLOY_SSH_KEY`** - приватный SSH ключ (весь ключ, включая BEGIN/END):
     ```
     -----BEGIN OPENSSH PRIVATE KEY-----
     ...содержимое ключа...
     -----END OPENSSH PRIVATE KEY-----
     ```
   - **`DEPLOY_PORT`** - порт SSH (по умолчанию 22, можно не указывать)
   - **`DEPLOY_PATH`** - путь к директории проекта на сервере (по умолчанию `/opt/newsagent`)
   
   **⚠️ ВАЖНО про доступ к GitHub Container Registry:**
   
   Workflow автоматически использует `GHCR_TOKEN` (если задан) или `GITHUB_TOKEN` для логина в registry.
   
   **Проблема:** Автоматический `GITHUB_TOKEN` часто не имеет прав на чтение packages из приватных репозиториев.
   
   **✅ РЕКОМЕНДУЕТСЯ: Использовать Personal Access Token**
   
   1. **Создайте Personal Access Token:**
      - Перейдите: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
      - Нажмите "Generate new token (classic)"
      - Название: `GHCR_READ_PACKAGES` (или любое другое)
      - Срок действия: выберите нужный (например, "No expiration" для долгосрочного использования)
      - **Права:** Отметьте только `read:packages` (в разделе "read")
      - Нажмите "Generate token"
      - **ВАЖНО:** Скопируйте токен сразу, он больше не будет показан!
   
   2. **Добавьте токен в GitHub Secrets:**
      - Перейдите в репозиторий → Settings → Secrets and variables → Actions
      - Нажмите "New repository secret"
      - Name: `GHCR_TOKEN`
      - Value: вставьте скопированный Personal Access Token
      - Нажмите "Add secret"
   
   3. **Проверка:**
      - Workflow автоматически будет использовать `GHCR_TOKEN` вместо `GITHUB_TOKEN`
      - При следующем деплое логин должен пройти успешно
   
   **Альтернатива: Использовать автоматический GITHUB_TOKEN**
   - Работает только для публичных репозиториев
   - Для приватных репозиториев нужно настроить права в Settings → Actions → General → Workflow permissions

**Важно:**
- Копируйте **приватный** ключ (не публичный!)
- Включайте все строки, включая BEGIN и END
- Не добавляйте лишних пробелов или переносов строк

### 7. Настройте доступ к GitHub Container Registry на сервере

```bash
# Создайте Personal Access Token в GitHub:
# Settings → Developer settings → Personal access tokens → Tokens (classic)
# Права: read:packages

# На сервере:
echo "YOUR_GITHUB_TOKEN" | docker login ghcr.io -u YOUR_USERNAME --password-stdin
```

Или добавьте в `.env` на сервере:
```bash
GITHUB_TOKEN=your_github_token
```

## Первый деплой

### Вариант 1: Автоматический (после push в main)

1. Убедитесь что все секреты настроены
2. Сделайте push в ветку `main`
3. Workflow автоматически соберет образ и задеплоит

### Вариант 2: Ручной запуск

1. Перейдите в Actions → Deploy to Server
2. Нажмите "Run workflow"
3. Выберите environment (production/staging)
4. Нажмите "Run workflow"

## Проверка деплоя

После деплоя проверьте:

```bash
# На сервере
cd /opt/newsagent
docker-compose -f docker-compose.prod.yml ps
docker-compose -f docker-compose.prod.yml logs -f

# Проверка метрик
curl http://localhost:8000/metrics
```

### Автоматическая диагностика метрик

Если метрики не работают, используйте скрипт диагностики:

```bash
# Скопируйте скрипт на сервер (с вашего компьютера)
scp scripts/diagnose_metrics.sh user@server:/opt/newsagent/

# На сервере запустите диагностику
cd /opt/newsagent
chmod +x diagnose_metrics.sh
./diagnose_metrics.sh
```

Скрипт проверит все аспекты работы метрик и даст рекомендации по исправлению проблем.

Подробнее см. [CHECK_METRICS.md](CHECK_METRICS.md#8-диагностика-на-сервере) в папке `docs/`

## Обновление кода на сервере

Если нужно обновить конфигурационные файлы (docker-compose.prod.yml, alloy.config.river):

```bash
# На сервере
cd /opt/newsagent
git pull  # если репозиторий клонирован
# или скопируйте файлы вручную
docker-compose -f docker-compose.prod.yml up -d
```

## Troubleshooting

### Ошибка: "Permission denied (publickey)"

- Проверьте что SSH ключ добавлен в GitHub Secrets
- Проверьте что публичный ключ добавлен на сервер: `~/.ssh/authorized_keys`

### Ошибка: "unauthorized: authentication required" или "error from registry: denied"

- Проверьте что на сервере настроен доступ к ghcr.io
- Проверьте что `GITHUB_TOKEN` имеет права `read:packages`
- Если репозиторий private, убедитесь что GITHUB_TOKEN имеет доступ к нему
- Попробуйте создать Personal Access Token с правами `read:packages` и использовать его вместо автоматического GITHUB_TOKEN

### Ошибка: "No such file or directory"

- Проверьте что DEPLOY_PATH указан правильно
- Убедитесь что файлы docker-compose.prod.yml и alloy.config.river существуют на сервере

### Health check failed

- Проверьте логи: `docker-compose -f docker-compose.prod.yml logs newsagent`
- Убедитесь что порт 8000 доступен
- Проверьте что .env файл настроен правильно

## Откат к предыдущей версии

```bash
# На сервере
cd /opt/newsagent
docker-compose -f docker-compose.prod.yml pull newsagent:main-<old-commit-sha>
docker-compose -f docker-compose.prod.yml up -d
```

