import uuid
from fastapi import Request

async def add_request_id_middleware(request: Request, call_next):
    # 1. Генерируем ID 
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    
    # 2. Сохраняем в state 
    request.state.request_id = request_id
    
    # 3. Вызываем следующий обработчик
    response = await call_next(request)
    
    # 4. Добавляем ID в заголовок ответа
    response.headers["X-Request-ID"] = request_id
    return response