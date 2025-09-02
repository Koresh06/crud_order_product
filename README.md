# CRUD Orders & Products API

## Описание

Проект реализует REST API для управления заказами (`Order`) и товарами (`Product`) с двумя версиями API:

* **v1** — ограниченная версия
* **v2** — полная версия

База данных: SQLite. Миграции применяются автоматически при запуске.

---

## Запуск проекта

1. Распакуйте архив в удобную папку / скачать репозиторий с GitHub.

2. Перейти в корневую папку проекта: 

```bash
cd crud_order_product
```

3. Запустите контейнеры через Docker Compose:

```bash
docker compose build
docker compose up -d
```

4. Примените миграции для обеих версий:
```bash
docker compose exec app_v1 alembic upgrade head 
docker compose exec app_v2 alembic upgrade head
```

5. API будет доступно по адресам:

* Версия v1: [http://localhost:8055](http://localhost:8055)
* Версия v2: [http://localhost:8050](http://localhost:8050)

Swagger-документация:

* v1: [http://localhost:8055/docs](http://localhost:8055/docs)
* v2: [http://localhost:8050/docs](http://localhost:8050/docs)

