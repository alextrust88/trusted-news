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

