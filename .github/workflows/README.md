# GitHub Actions Workflows

Этот каталог содержит конфигурации для GitHub Actions CI/CD.

## Основной Workflow

### CI/CD Pipeline (`.github/workflows/ci-cd.yml`) ⭐

**Главный workflow** - выполняет все шаги последовательно:

1. **Тесты** (`test`, `lint`) - запускаются параллельно
2. **Сборка образа** (`build`) - только после успешных тестов
3. **Деплой** (`deploy`) - только после успешной сборки и только для `main`

**Триггеры:**
- Push в ветки `main` или `develop`
- Pull Request в ветки `main` или `develop`
- Ручной запуск через `workflow_dispatch`

**Последовательность выполнения:**
```
Тесты (test + lint) → Сборка образа (build) → Деплой (deploy)
```

## Структура Workflow

### Jobs и их зависимости

```
test ──┐
       ├──> build ──> deploy
lint ──┘
```

- **test** и **lint** - выполняются параллельно
- **build** - ждет завершения test и lint
- **deploy** - ждет завершения build, запускается только для ветки `main`

## Настройка секретов

1. Перейдите в Settings → Secrets and variables → Actions
2. Добавьте необходимые секреты (см. DEPLOY.md)

## Ручной запуск деплоя

1. Перейдите в Actions → CI/CD Pipeline
2. Нажмите "Run workflow"
3. Выберите environment (production/staging)
4. Нажмите "Run workflow"

## Отладка

Если workflow не работает:
1. Проверьте логи в разделе Actions
2. Убедитесь что все секреты настроены
3. Проверьте что SSH ключ правильный
4. Проверьте что на сервере установлены Docker и Docker Compose
