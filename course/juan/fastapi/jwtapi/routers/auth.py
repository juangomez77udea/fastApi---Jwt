from fastapi import APIRouter, HTTPException, Request, status
from fastapi.params import Depends

from course.juan.fastapi.jwtapi.dependencies.di import get_repository
from course.juan.fastapi.jwtapi.repositories.user_repository import UserRepository
from course.juan.fastapi.jwtapi.schemas.auth import LoginInRequest, TokenDto
from course.juan.fastapi.jwtapi.security.passwords import verify_password
from course.juan.fastapi.jwtapi.services.jwt import create_access_token

router = APIRouter()

# Swagger (boton Authorize) envia un form x-www-form-urlencoded con username/password,
# Postman puede enviar JSON con email/password. Se documentan ambos formatos.
_LOGIN_OPENAPI = {
    "requestBody": {
        "required": True,
        "content": {
            "application/x-www-form-urlencoded": {
                "schema": {
                    "type": "object",
                    "required": ["username", "password"],
                    "properties": {
                        "username": {"type": "string", "description": "Email del usuario"},
                        "password": {"type": "string", "format": "password"},
                    },
                }
            },
            "application/json": {"schema": LoginInRequest.model_json_schema()},
        },
    }
}


async def get_credentials(request: Request) -> LoginInRequest:
    content_type = request.headers.get('content-type', '')
    try:
        if content_type.startswith('application/json'):
            data = await request.json()
            username = data.get('email') or data.get('username')
        else:
            data = await request.form()
            username = data.get('username') or data.get('email')
        password = data.get('password')
    except Exception:
        username = password = None

    if not username or not password:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="username/email and password are required")
    return LoginInRequest(email=str(username), password=str(password))


@router.post('/token', response_model=TokenDto, openapi_extra=_LOGIN_OPENAPI)
async def login(
    credentials: LoginInRequest = Depends(get_credentials),
    repository: UserRepository = Depends(get_repository),
):
    user = repository.find_by_email(credentials.email)
    if not user or not verify_password(credentials.password, str(user.password)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales no validas")

    token = create_access_token(subject=str(user.id))
    return TokenDto(access_token=token)
