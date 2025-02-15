## Проект использует Django и Django Rest Framework (DRF) для создания RESTful API.
---
### Основные шаги по установке, настройке и использованию API, а также описания доступных эндпоинтов.

##### ***1. Создание виртуального окружения***

Предварительные требования

Перед началом работы убедитесь, что у вас установлены:

Docker

Docker Compose

##### ***2. Установка и запуск***

Клонируйте репозиторий

git clone <репозиторий>
cd <папка_проекта>

Создайте файл окружения .env

touch .env

Отредактируйте .env, указав нужные значения (например, для базы данных):

##### Хост PostgreSQL
POSTGRES_HOST
##### Порт PostgreSQL
POSTGRES_PORT
##### Имя пользователя для подключения
POSTGRES_USER
##### Пароль пользователя
POSTGRES_PASSWORD
##### Название базы данных
POSTGRES_DB

Запустите контейнеры

docker-compose up -d --build

Это запустит приложение в фоновом режиме.

Создайте суперпользователя для Django Admin

docker-compose exec service_terminology_app python manage.py createsuperuser

Введите логин, email и пароль при запросе.

##### 3. Доступ к API и интерфейсам

Swagger UI

http://127.0.0.1:8000/swagger/

Административная панель

http://127.0.0.1:8000/admin/

API Эндпоинты

##### 1. Получение списка справочников

Метод: GET

URL: /api/refbooks/?date=

Параметры запроса:

date (опционально) — дата, на которую запрашивается список справочников.

##### 2. Получение элементов для версии заданного справочника

Метод: GET

URL: /api/refbooks/{id}/elements/?version=

Параметры запроса:

version (опционально) — версия справочника.

##### 3. Валидация элемента справочника

Метод: GET

URL: /api/refbooks/{id}/check_element?code={code}&value={value}[&version={version}]

Параметры запроса:

code — код элемента.

value — значение элемента.

version (опционально) — версия справочника.

