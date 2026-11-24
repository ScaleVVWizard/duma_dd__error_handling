# Лабораторная работа №8. Обработка ошибок, валидация и логирование в FastAPI

**Студент:** Дума Данил КБ-241
**GitHub:** https://github.com/ScaleVVWizard/duma_dd__error_handling

## Выполненные пункты

### №0. Подготовительный этап: создание проекта и первого коммита

Создана новая директория `duma_dd__error_handling`, инициализирован git-репозиторий (`git init`), скачан стандартный `.gitignore` для Python и добавлена строка `.env`:

![git init и .gitignore](shots/2-1.PNG)

Проект инициализирован через `uv init`, создано виртуальное окружение (`uv venv`), установлены зависимости (`fastapi`, `uvicorn`, `pydantic`, `pydantic-settings`, `loguru`). Создана структура директорий `app/` с файлами `main.py`, `config.py`, `exceptions.py`, `handlers.py`, `logging_config.py`, `schemas.py` и папкой `routers/`:

![uv init, структура и установка зависимостей](shots/2-2.PNG)

В `app/config.py` создан класс настроек на базе `pydantic-settings`:

![config.py](shots/2-3.PNG)

В `app/main.py` создано минимальное приложение FastAPI с подключением роутеров и корневым маршрутом:

![main.py](shots/2-4.PNG)

Созданы заготовки для роутеров: `users.py` и `test_routes.py` с базовыми `APIRouter`:

![routers/users.py](shots/2-5.PNG)
![routers/test_routes.py](shots/2-6.PNG)

Роутеры экспортированы в `app/routers/__init__.py`:

![routers/__init__.py](shots/2-7.PNG)

Приложение запущено через `uvicorn app.main:app --reload`. Проверка доступности Swagger UI (`/docs`):

![Запуск и Swagger](shots/2-8.PNG)

Сделан первый коммит с базовой структурой проекта:

![Первый коммит](shots/2-9.PNG)

### №1. Пользовательские исключения и обработчики

В `app/exceptions.py` определены два пользовательских исключения (`CustomExceptionA` с кодом 409 и `CustomExceptionB` с кодом 404):

![exceptions.py](shots/2-10.PNG)

В `app/schemas.py` создана единая модель ответа об ошибке `ErrorResponse`:

![schemas.py](shots/2-11.PNG)

В `app/handlers.py` зарегистрированы обработчики для этих исключений, возвращающие `ErrorResponse`:

![handlers.py](shots/2-12.PNG)

Обработчики подключены в `app/main.py`:

![main.py с обработчиками](shots/2-13.PNG)

Созданы тестовые эндпоинты в `app/routers/test_routes.py`, которые вызывают эти исключения:

![test_routes.py](shots/2-14.PNG)

Проверка: `GET /test/a/-5` возвращает 409 с телом `ErrorResponse`:

![Тест A](shots/2-15.PNG)

Проверка: `GET /test/b/200` возвращает 404 с телом `ErrorResponse`:

![Тест B](shots/2-16.PNG)

Сделан коммит с добавлением пользовательских исключений и обработчиков:

![Коммит](shots/2-17.PNG)

### №2. Логирование ошибок с контекстом (Loguru)

Создан файл `app/logging_config.py` с настройкой логгера, маскированием чувствительных заголовков (`authorization`, `cookie`) и полей тела (`password`, `token`), а также записью в файл с ротацией:

![logging_config.py](shots/2-18.PNG)

Логгер интегрирован в обработчики ошибок в `app/handlers.py`. Добавлен глобальный обработчик для перехвата всех непредвиденных исключений:

![handlers.py с логгером](shots/2-19.PNG)

Глобальный обработчик подключен в `app/main.py`:

![main.py с global_exception_handler](shots/2-20.PNG)

В `app/routers/test_routes.py` добавлены тестовые маршруты `/boom` (для вызова `RuntimeError`) и `/echo` (для проверки маскирования):

![test_routes.py с boom и echo](shots/2-21.PNG)

Запуск приложения:

![Запуск сервера](shots/2-22.PNG)

Проверка `GET /test/boom` в Swagger UI возвращает 500 Internal Server Error с единым форматом `ErrorResponse`:

![Тест boom в Swagger](shots/2-23.PNG)

В консоли сервера при вызове `/test/boom` логируется полный трейсбек с контекстом запроса:

![Трейсбек в консоли](shots/2-24.PNG)

Проверка `POST /test/echo` через curl с телом `{"password": "secret", "data": "test"}`:

![Тест echo через curl](shots/2-25.PNG)

В логах сервера видно, что поле `password` успешно замаскировано на `***`:

![Маскирование в логах](shots/2-26.PNG)

Сделан коммит с добавлением логирования ошибок с контекстом и маскировкой:

![Коммит](shots/2-27.PNG)

### №3. Валидация данных и кастомная обработка ошибок валидации

В `app/schemas.py` добавлена модель пользователя `UserCreate` с валидационными ограничениями (длина логина, возраст > 18, формат email, длина пароля):

![UserCreate в schemas.py](shots/2-28.PNG)

В `app/handlers.py` создан обработчик для `RequestValidationError`, который формирует детальный список ошибок по полям:

![validation_exception_handler в handlers.py](shots/2-29.PNG)

Обработчик подключен в `app/main.py`:

![Подключение в main.py](shots/2-30.PNG)

В `app/routers/users.py` создан эндпоинт `POST /users/register`:

![users.py](shots/2-31.PNG)

В `app/routers/test_routes.py` обновлены тестовые маршруты (добавлены `/boom` и `/echo`):

![test_routes.py](shots/2-32.PNG)

Проверка в Swagger UI: отправка невалидного JSON (короткий логин, возраст 17, неверный email, короткий пароль) возвращает 422 с массивом ошибок в `details`:

![Невалидный запрос](shots/2-33.PNG)

Проверка: отправка валидного JSON возвращает 200 OK с именем и email пользователя:

![Валидный запрос](shots/2-34.PNG)

В логах сервера видны запросы с кодами 422 и 200:

![Логи в консоли](shots/2-35.PNG)

Сделан коммит с реализацией Problem Details:

![Коммит](shots/2-36.PNG)

### №4. Problem Details для ошибок валидации (422)

В `app/schemas.py` добавлены модели `ValidationErrorDetail` и `ProblemDetails` для соответствия стандарту RFC 9457:

![ProblemDetails в schemas.py](shots/2-37.PNG)

Обработчик `validation_exception_handler` в `app/handlers.py` модифицирован для возврата `ProblemDetails` с заголовком `Content-Type: application/problem+json`:

![Обновленный обработчик](shots/2-38.PNG)

В `app/routers/users.py` добавлена документация для эндпоинта `POST /users/register` с указанием возможного ответа 422 и примером:

![Документация в users.py](shots/2-39.PNG)

Проверка в Swagger UI: отправка невалидного JSON возвращает 422 с телом в формате `ProblemDetails` (`type`, `title`, `status`, `detail`, `instance`, `errors`):

![Невалидный запрос в Swagger](shots/2-40.PNG)

В консоли сервера видно, что `RequestValidationError` перехвачен, и в логах отображаются детали ошибки:

![Логи в консоли](shots/2-41.PNG)

Сделан коммит с реализацией Problem Details для 422 и документацией Swagger:

![Коммит](shots/2-42.PNG)

### №5.1. Самостоятельная работа: middleware для X-Request-ID

Создан файл `app/middleware.py` с функцией `add_request_id_middleware`, которая генерирует уникальный ID для каждого запроса, добавляет его в `request.state.request_id` и в заголовок ответа `X-Request-ID`:

![middleware.py](shots/2-43.PNG)

Middleware подключен в `app/main.py`:

![Подключение в main.py](shots/2-44.PNG)

Проверка в Swagger UI: в ответе на запрос с ошибкой валидации (422) присутствует заголовок `x-request-id`:

![Ответ с x-request-id](shots/2-45.PNG)

В логах (файл `app.log`) видно, что `request_id` передается в контекст и используется при логировании ошибки:

![Логи с request_id](shots/2-46.PNG)

Сделан коммит с добавлением middleware:

![Коммит](shots/2-47.PNG)

### №5.2. Самостоятельная работа: обработчик HTTPException

В `app/handlers.py` добавлен кастомный обработчик `http_exception_handler`, который логирует ошибки `HTTPException` и возвращает единый формат `ErrorResponse`:

![Обработчик HTTPException](shots/2-48.PNG)

Обработчик подключен в `app/main.py`:

![Подключение в main.py](shots/2-49.PNG)

В `app/routers/test_routes.py` добавлен тестовый маршрут `/test/http-error`, который вызывает `HTTPException` со статусом 403:

![Маршрут http-error](shots/2-50.PNG)

Проверка в Swagger UI: запрос `GET /test/http-error` возвращает 403 с телом `ErrorResponse` и заголовком `x-request-id`:

![Проверка HTTPException](shots/2-51.PNG)

Сделан коммит с добавлением кастомного обработчика `HTTPException`:

![Коммит](shots/2-52.PNG)

### №5.3. Самостоятельная работа: валидация сложных паролей

В `app/schemas.py` в модель `UserCreate` добавлен `@field_validator` для проверки сложности пароля: он должен содержать как минимум одну цифру и один специальный символ:

![Валидатор пароля](shots/2-53.PNG)

Проверка в Swagger UI: при отправке пароля без цифры (`securepwd`) возвращается 422 с сообщением `Password must contain at least one digit`:

![Ошибка: нет цифры](shots/2-54.PNG)

Проверка: при отправке пароля без спецсимвола (`securepwd1`) возвращается 422 с сообщением `Password must contain at least one special character`:

![Ошибка: нет спецсимвола](shots/2-55.PNG)

Проверка: при отправке пароля, содержащего и цифру, и спецсимвол (`securepwd1!`), запрос проходит успешно (200 OK):

![Успешный запрос](shots/2-56.PNG)

### №5.4. Самостоятельная работа: тесты для проверки обработки ошибок

Установлены зависимости `pytest`, `httpx` и `pytest-asyncio`:

![Установка зависимостей](shots/2-57.PNG)

Создан файл `tests.py`, в котором написаны тесты для проверки `CustomExceptionA`, `CustomExceptionB`, `RequestValidationError`, `HTTPException` и неожиданного исключения (`RuntimeError`):

![Код тестов](shots/2-58.PNG)

Запуск тестов через `pytest`: все 5 тестов успешно пройдены:

![Результаты тестов](shots/2-59.PNG)

Сделан коммит с добавлением тестов:

![Коммит тестов](shots/2-60.PNG)

### №5.5. Самостоятельная работа: ротация логов по размеру файла

В `app/logging_config.py` в конфигурацию Loguru добавлена ротация при достижении размера файла 10 МБ (параметр `rotation="10 MB"`):

![Ротация по размеру](shots/2-61.PNG)

Сделан коммит с добавлением ротации логов по размеру:

![Коммит ротации](shots/2-62.PNG)

