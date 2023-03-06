# Дипломный проект сайт Foodgram
---

*foodgram-project-react*


### Статус workflow
[![Foodgram workflow](https://github.com/AlGenSo/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)](https://github.com/AlGenSo/foodgram-project-react/actions/workflows/foodgram_workflow.yml)
---

### Описание

##### Идея проекта
Создать приложение «Продуктовый помощник»: сайт, на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.
На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.


##### Задача проекта
Написать бэкенд проекта и **API** для него (приложение **api**)

Настроить для приложения Continuous Integration и Continuous Deployment.


### Технологии:
- Django
- Django REST Framework
- Django Filter
- PyJWT
- Djoser
- Docker
- PostgreSQL
- Nginx
- Gunicorn
- DockerHub
- Yandex.Cloud


### Установка
##### Требования для корректной работы

[python 3.7](https://www.python.org/downloads/), django 3.2


##### Для тестирования запросов можно использовать
[Postman](https://www.postman.com/downloads/)


##### Запуск проекта

* _Клонировать репозиторий: `git clone` git@github.com:AlGenSo/foodgram-project-react.git
* _Перейти в него в командной строке: `cd foodgram-project-react`_
* _Cоздать виртуальное окружение: `python -m venv venv`_
* _Обновить pip: `python -m pip install --upgrade pip`_
* _Перейти в папку backend в командной строке: `cd backend`_
* _Установить зависимости из файла requirements.txt: `pip install -r requirements.txt`_
* _Выполнить миграции: `python manage.py migrate`_

##### Запуск локально

* _Перейти в папку infra в командной строке: `cd.. -> cd infra`_
* _Собрать образ при помощи docker-compose: $ docker-compose up -d --build_
* _Выполнить по почереди следующие команды:_

```
   docker-compose exec backend python manage.py migrate #  Вполнить миграции
   docker-compose exec backend python manage.py createsuperuser # Создать суперюзера
   docker-compose exec backend python manage.py collectstatic --no-input # Собрать статику
   docker-compose exec backend python manage.py load_csv # загрузить ингредиенты и теги в БД
```


#### Полсе запуска будет доступна документация

[ReDpc](http://localhost/api/docs/)

[Админка](http://localhost/admin/)

* _Доступ в админку:_
```
email: *******
passowrd: adminadmin
```
