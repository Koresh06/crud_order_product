# CRUD Orders & Products API

## Описание

Проект реализует REST API для управления заказами (`Order`) и товарами (`Product`) с двумя версиями API:

* **v1** — ограниченная версия
* **v2** — полная версия

База данных: SQLite. Миграции применяются автоматически при запуске.

---

## Запуск проекта

1. Распакуйте архив в удобную папку.

2. Запустите контейнеры через Docker Compose:

```bash
docker-compose build
docker-compose up -d
```

4. API будет доступно по адресам:

* Версия v1: [http://localhost:8055](http://localhost:8055)
* Версия v2: [http://localhost:8050](http://localhost:8050)

Swagger-документация:

* v1: [http://localhost:8055/docs](http://localhost:8055/docs)
* v2: [http://localhost:8050/docs](http://localhost:8050/docs)

