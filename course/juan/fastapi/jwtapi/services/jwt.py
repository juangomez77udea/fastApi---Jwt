from datetime import datetime, timezone, timedelta

from jose import jwt

from course.juan.fastapi.jwtapi.config.settings import settings


def create_access_token(subject: str):

    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXP_MINUTES)
    payload = {'sub': subject, 'exp': expire}
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token