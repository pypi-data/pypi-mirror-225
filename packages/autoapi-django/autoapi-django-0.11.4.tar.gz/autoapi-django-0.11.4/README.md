# AutoAPI

AutoAPI собирает абстрагирует ваше приложение от слоя с передачей данных,
генерируя API из чистых классов, содержащих логику.

## Документация

- [Russian](./docs/autoapi/index.md)
- English (in future)

## Развертывание на локалке

Устанавливаем virtual env:

```shell
python3 -m venv venv
. venv/bin/activate
```

Устанавливаем библиотеку с зависимостями
```shell
pip install .
```

Переходим в example-проект, мигрируем БД (SQLite) и запускаем:
```shell
cd example/online_shop
python manage.py migrate
python manage.py runserver
```

По урле http://127.0.0.1:8000/docs/ будет доступен Swagger для сгенерированного API.
Оттуда можно дергать хэндлеры.

Рекомендуется создать суперюзера (`python manage.py createsuperuser`) и авторизоваться в админке.
Чтобы проверить корректную работу API, можно дернуть хэндлер `user.get_user` в сваггере.


Для билда и отправки в PyPI надо сделать:
```shell
pip install build
python -m build
pip install twine
twine upload dist/*
```
