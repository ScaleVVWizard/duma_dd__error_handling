from fastapi import APIRouter, status
from app.schemas import UserCreate, ProblemDetails

router = APIRouter(prefix="/users", tags=["users"])

@router.post(
    "/register",
    responses={
        422: {
            "description": "Validation Error",
            "content": {
                "application/problem+json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "type": {"type": "string", "example": "https://example.com/problems/validation-error"},
                            "title": {"type": "string", "example": "Validation Error"},
                            "status": {"type": "integer", "example": 422},
                            "detail": {"type": "string", "example": "The request body failed validation."},
                            "instance": {"type": "string", "example": "/users/register"},
                            "errors": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "field": {"type": "string", "example": "age"},
                                        "message": {"type": "string", "example": "ensure this value is greater than 18"},
                                        "code": {"type": "string", "example": "value_error"}
                                    }
                                }
                            }
                        }
                    },
                    "example": {
                        "type": "https://example.com/problems/validation-error",
                        "title": "Validation Error",
                        "status": 422,
                        "detail": "The request body failed validation.",
                        "instance": "/users/register",
                        "errors": [
                            {"field": "age", "message": "ensure this value is greater than 18", "code": "value_error"},
                            {"field": "email", "message": "value is not a valid email address", "code": "value_error"}
                        ]
                    }
                }
            }
        }
    }
)
async def register(user: UserCreate):
    return {"username": user.username, "email": user.email}