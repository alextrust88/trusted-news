# Troubleshooting деплоя

## Ошибка: "docker: command not found"

**Проблема:** Docker не установлен или не в PATH.

**Решение:**

1. **Установите Docker на сервере:**
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

2. **Добавьте пользователя в группу docker:**
```bash
sudo usermod -aG docker $USER
newgrp docker  # или перелогиньтесь
```

3. **Проверьте установку:**
```bash
docker --version
docker ps
```

## Ошибка: "docker-compose: command not found"

**Проблема:** Docker Compose не установлен.

**Решение:**

### Вариант 1: Docker Compose Plugin (рекомендуется)

```bash
# Установите plugin
sudo apt-get update
sudo apt-get install docker-compose-plugin

# Используется как: docker compose (с пробелом)
docker compose version
```

### Вариант 2: Старый docker-compose

```bash
# Установите отдельный бинарник
sudo apt-get install docker-compose

# Используется как: docker-compose (с дефисом)
docker-compose --version
```

**Примечание:** Workflow автоматически определяет какой вариант использовать.

## Ошибка: "Permission denied" при выполнении docker

**Проблема:** Пользователь не в группе docker.

**Решение:**

```bash
# Добавьте пользователя в группу docker
sudo usermod -aG docker $USER

# Примените изменения (выберите один вариант):
newgrp docker
# или
su - $USER
# или перелогиньтесь в систему
```

## Проверка перед деплоем

Выполните на сервере:

```bash
# 1. Проверка Docker
docker --version
docker ps

# 2. Проверка Docker Compose
docker compose version || docker-compose --version

# 3. Проверка прав
docker ps  # должно работать без sudo

# 4. Проверка доступа к ghcr.io
docker login ghcr.io
# Введите ваш GitHub username и Personal Access Token
```

## Быстрая установка всего необходимого

```bash
# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Установка Docker Compose plugin
sudo apt-get update
sudo apt-get install -y docker-compose-plugin

# Добавление пользователя в группу docker
sudo usermod -aG docker $USER
newgrp docker

# Проверка
docker --version
docker compose version
docker ps
```

## Если Docker установлен, но не работает

1. **Проверьте статус службы:**
```bash
sudo systemctl status docker
sudo systemctl start docker
sudo systemctl enable docker
```

2. **Проверьте PATH:**
```bash
which docker
echo $PATH
```

3. **Проверьте права:**
```bash
ls -la /usr/bin/docker
groups  # должен содержать 'docker'
```

## Ошибка: "lookup ghcr.io timeout" или "dial tcp: lookup ghcr.io"

**Проблема:** Сервер не может разрешить DNS имя `ghcr.io`.

**Причины:**
- Проблемы с DNS сервером на сервере
- Проблемы с интернет-соединением
- Firewall блокирует DNS запросы
- Неправильная конфигурация сети

**Решение:**

### Шаг 1: Проверьте интернет-соединение

```bash
# Проверка ping до Google DNS
ping -c 4 8.8.8.8

# Проверка DNS
nslookup ghcr.io
# или
dig ghcr.io
```

### Шаг 2: Измените DNS сервер

```bash
# Редактируйте /etc/resolv.conf
sudo nano /etc/resolv.conf

# Добавьте или замените на:
nameserver 8.8.8.8
nameserver 1.1.1.1
nameserver 8.8.4.4
```

**Для Ubuntu/Debian с systemd-resolved:**
```bash
sudo systemd-resolve --status
sudo systemd-resolve --set-dns=8.8.8.8 --interface=eth0
```

**Для Ubuntu/Debian с NetworkManager:**
```bash
sudo nmcli connection modify "your-connection-name" ipv4.dns "8.8.8.8 1.1.1.1"
sudo nmcli connection down "your-connection-name"
sudo nmcli connection up "your-connection-name"
```

### Шаг 3: Временное решение - добавить в /etc/hosts

```bash
# Узнайте IP адрес ghcr.io
GHCR_IP=$(dig +short ghcr.io | head -1)

# Добавьте в /etc/hosts
echo "$GHCR_IP ghcr.io" | sudo tee -a /etc/hosts

# Проверка
ping -c 2 ghcr.io
```

### Шаг 4: Проверьте firewall

```bash
# Проверьте что DNS порт 53 открыт
sudo ufw status
# или
sudo iptables -L

# Если нужно, разрешите DNS
sudo ufw allow 53/tcp
sudo ufw allow 53/udp
```

### Шаг 5: Проверьте после изменений

```bash
# Проверка DNS
nslookup ghcr.io

# Проверка доступности
curl -I https://ghcr.io

# Попробуйте логин вручную
echo "YOUR_TOKEN" | docker login ghcr.io -u YOUR_USERNAME --password-stdin
```

## Ошибка: "error from registry: denied" при pull образа

**Проблема:** Нет доступа к GitHub Container Registry.

**Причины:**
- `GITHUB_TOKEN` не имеет прав `read:packages`
- Репозиторий приватный и `GITHUB_TOKEN` не имеет доступа
- Проблемы с сетью/DNS на сервере

**Решение:**

### Шаг 1: Создайте Personal Access Token

1. Перейдите: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Нажмите "Generate new token (classic)"
3. Название: `GHCR_READ_PACKAGES`
4. Срок действия: выберите нужный
5. **Права:** Отметьте только `read:packages` (в разделе "read")
6. Нажмите "Generate token"
7. **ВАЖНО:** Скопируйте токен сразу!

### Шаг 2: Добавьте токен в GitHub Secrets

1. Репозиторий → Settings → Secrets and variables → Actions
2. Нажмите "New repository secret"
3. Name: `GHCR_TOKEN`
4. Value: вставьте скопированный токен
5. Нажмите "Add secret"

### Шаг 3: Проверка

Workflow автоматически будет использовать `GHCR_TOKEN` вместо `GITHUB_TOKEN`.

**Проверьте что образ существует:**
```bash
# На вашем компьютере (с вашим токеном)
echo "YOUR_TOKEN" | docker login ghcr.io -u YOUR_USERNAME --password-stdin
docker pull ghcr.io/alextrust88/trusted-news:latest
```

## Ошибка: "env file /opt/newsagent/.env not found"

**Проблема:** Файл `.env` не создан на сервере.

**Решение:**

1. **Создайте файл `.env` на сервере:**
```bash
cd /opt/newsagent
nano .env
```

2. **Добавьте необходимые переменные:**
```bash
TELEGRAM_BOT_TOKEN=ваш_токен
TELEGRAM_CHAT_ID=ваш_chat_id
METRICS_PORT=8000
```

3. **Установите правильные права:**
```bash
chmod 600 .env
```

4. **Проверьте:**
```bash
ls -la .env
cat .env  # убедитесь что файл читается
```

