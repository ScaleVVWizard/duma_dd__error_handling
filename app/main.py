from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from app.config import settings
from app.routers import users_router, test_router
from app.exceptions import CustomExceptionA, CustomExceptionB
from app.handlers import (
    custom_exception_a_handler, 
    custom_exception_b_handler, 
    global_exception_handler,
    validation_exception_handler
)
from app.middleware import add_request_id_middleware

app = FastAPI(title=settings.app_name)

# Подключаем middleware для генерации X-Request-ID
app.middleware("http")(add_request_id_middleware)

# Подключаем обработчики ошибок
app.add_exception_handler(CustomExceptionA, custom_exception_a_handler)
app.add_exception_handler(CustomExceptionB, custom_exception_b_handler)
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Подключаем роутеры
app.include_router(users_router)
app.include_router(test_router)

@app.get("/")
async def root():
    return {"message": "Hello, Error Handling Lab!"}