# NeKidaem тестовое #1
## Blog REST API

Имеется возможность подписываться на блоги пользователей и делать посты.
Пользователи добавляются **ТОЛЬКО** через админку!

## Используемый стек

[![Python][Python-badge]][Python-url]
[![Django][Django-badge]][Django-url]
[![DRF][DRF-badge]][DRF-url]
[![Postgres][Postgres-badge]][Postgres-url]
[![Nginx][Nginx-badge]][Nginx-url]

## Задание

Задание можно посмотреть по этой ссылке [click](
https://wiki.nekidaem.ru/s/test-rest-api-python
)

## Архитектура проекта

| Директория    | Описание                                                |
|---------------|---------------------------------------------------------|
| `infra`       | Файлы для запуска с помощью Docker, настройки Nginx     |
| `src/backend` | Код Django приложения                                   |


# Подготовка

## Требования

1. **Python 3.12**  
   Убедитесь, что у вас установлена нужная версия Python или активирована в
   pyenv.

2. **Poetry**  
   Зависимости и пакеты управляются через poetry. Убедитесь, что
   poetry [установлен](https://python-poetry.org/docs/#installing-with-the-official-installer)
   на вашем компьютере и ознакомьтесь
   с [документацией](https://python-poetry.org/docs/basic-usage/).  
   Установка зависимостей

    ```
    poetry install
    ```

    Также будет создано виртуальное окружение, если привычнее видеть его в
    директории проекта, то
    используйте [настройку](https://python-poetry.org/docs/configuration/#adding-or-updating-a-configuration-setting) `virtualenvs.in-project`


3. **Docker**

4. **pre-commit (если хотите поиграться с проектом)**
   [Документация](https://pre-commit.com/)  
   При каждом коммите выполняются хуки (автоматизации) перечисленные в
   .pre-commit-config.yaml. Если не понятно какая ошибка мешает сделать коммит
   можно запустить хуки вручную и посмотреть ошибки:
    ```shell
    pre-commit run --all-files
    ```
   Для упрощения можно установить `pre-commit`
   ```shell
   pre-commit install
   ```

# Разворачиваем проект в контейнерах
Создаём `.env` файл в корневой директории проекта и заполняем его по
образцу `.env.example` и скопируйте его в папку `infra`

Переходим в директорию `infra/`

```shell
cd infra/
```

Поднимаем контейнеры
```shell
docker-compose -f docker-compose.dev.yml up -d
```

## Администрирование развёрнутого приложения
### Создание суперпользователя
Используйте команду ниже и следуйте инструкциям в терминале (перед этим
откройте новое окно)
```shell
docker exec -it backend python manage.py createsuperuser
```

# Разворачиваем проект локально

Устанавливаем зависимости

Создаём `.env` файл в корневой директории проекта и заполняем его по
образцу `.env.example`

Переходим в директорию `src/backend/`

```shell
cd src/backend/
```

Применяем миграции

```shell
python manage.py migrate
```

Загружаем фикстуры (локации)

```shell
python manage.py import_locations
```

Запускаем *development*-сервер *Django*

```shell
python manage.py runserver
```


<!-- MARKDOWN LINKS & BADGES -->

[Python-url]: https://www.python.org/

[Python-badge]: https://img.shields.io/badge/Python-376f9f?style=for-the-badge&logo=python&logoColor=white

[Django-url]: https://github.com/django/django

[Django-badge]: https://img.shields.io/badge/Django-0c4b33?style=for-the-badge&logo=django&logoColor=white

[DRF-url]: https://github.com/encode/django-rest-framework

[DRF-badge]: https://img.shields.io/badge/DRF-a30000?style=for-the-badge

[Postgres-url]: https://www.postgresql.org/

[Postgres-badge]: https://img.shields.io/badge/postgres-306189?style=for-the-badge&logo=postgresql&logoColor=white

[Nginx-url]: https://nginx.org

[Nginx-badge]: https://img.shields.io/badge/nginx-009900?style=for-the-badge&logo=nginx&logoColor=white
