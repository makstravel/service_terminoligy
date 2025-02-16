## Проект использует Django и Django Rest Framework (DRF) для создания RESTful API.
---
### Основные шаги по установке, настройке и использованию API, а также описания доступных эндпоинтов.
Предварительные требования

!!! Перед началом работы убедитесь, что у вас установлены: !!!

[Docker](https://www.docker.com/) -Docker

[Docker Compose](https://docs.docker.com/compose/install/)  - Docker Compose

##### ***1. Установка и запуск***

Клонируйте репозиторий

```git clone https://github.com/makstravel/service_terminoligy.git && cd service_terminoligy```


##### ***2. Создание виртуального окружения***
Создайте файл окружения .env

```touch .env```

Отредактируйте .env, указав нужные значения для базы данных:

##### Хост PostgreSQL
*POSTGRES_HOST=*
##### Порт PostgreSQL
*POSTGRES_PORT=*
##### Имя пользователя для подключения
*POSTGRES_USER=*
##### Пароль пользователя
*POSTGRES_PASSWORD=*
##### Название базы данных
*POSTGRES_DB=*

Запустите контейнеры

``` docker-compose up -d --build ```

Это запустит приложение в фоновом режиме.
-- при установке файл *entrypoint.sh* запускает миграции джанго, если вдруг не запустились миграциции то введите эту команду

```docker-compose exec service_terminology_app python manage.py migrate``` 

Создайте суперпользователя для Django Admin

```docker-compose exec service_terminology_app python manage.py createsuperuser```

Введите логин, email и пароль при запросе.


##### 3. Доступ к API и интерфейсам

Swagger UI

http://127.0.0.1:8000/swagger/

Административная панель

http://127.0.0.1:8000/admin/

## API Эндпоинты

#### 1. Получение списка справочников

Метод: GET

URL: /api/refbooks/?date=

Параметры запроса:

date (опционально) — дата, на которую запрашивается список справочников.

#### 2. Получение элементов для версии заданного справочника

Метод: GET

URL: /api/refbooks/{id}/elements/?version=

Параметры запроса:

version (опционально) — версия справочника.

#### 3. Валидация элемента справочника

Метод: GET

URL: /api/refbooks/{id}/check_element?code={code}&value={value}[&version={version}]

Параметры запроса:

code — код элемента.

value — значение элемента.

version (опционально) — версия справочника.

