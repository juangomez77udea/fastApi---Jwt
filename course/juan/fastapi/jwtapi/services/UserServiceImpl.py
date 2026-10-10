from typing import List

from sqlalchemy.orm import Session

from course.juan.fastapi.jwtapi.entities.user import User
from course.juan.fastapi.jwtapi.repositories.user_repository import UserRepository
from course.juan.fastapi.jwtapi.schemas.user_dto import UserDto
from course.juan.fastapi.jwtapi.schemas.user_request import UserRequest
from course.juan.fastapi.jwtapi.security.passwords import hash_password
from course.juan.fastapi.jwtapi.services.user_service import UserService


class UserServiceImpl(UserService):
    def __init__(self, repo: UserRepository, db:Session):
        self._repo = repo
        self._db = db

    def find_all(self) -> List[UserDto]:
        return [UserDto.model_validate(user) for user in self._repo.find_all()]

    def find_by_id(self, user_id: int) -> UserDto | None:
        user = self._repo.find_by_id(user_id)
        if not user:
            return None
        return UserDto.model_validate(user)

    def find_by_email(self, email: str) -> UserDto | None:
        user = self._repo.find_by_email(email)
        if not user:
            return None
        return UserDto.model_validate(user)

    def create(self, user: UserRequest) -> UserDto:
        if self._repo.find_by_email(str(user.email)):
            raise ValueError("Email already registered")
        user_entity = User(email=user.email, password= hash_password(user.password))
        try:
            self._repo.create(user_entity)
            self._db.commit()
            self._db.refresh(user_entity)
            return UserDto.model_validate(user_entity)
        except Exception:
            self._db.rollback()
            raise
