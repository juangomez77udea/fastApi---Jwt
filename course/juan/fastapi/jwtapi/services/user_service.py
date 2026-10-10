from abc import ABC, abstractmethod
from typing import List

from course.juan.fastapi.jwtapi.schemas.user_dto import UserDto
from course.juan.fastapi.jwtapi.schemas.user_request import UserRequest


class UserService(ABC):

    @abstractmethod
    def find_all(self) -> List[UserDto]:
        pass

    @abstractmethod
    def find_by_id(self, user_id: int) -> UserDto |None:
        pass

    @abstractmethod
    def create(self, user: UserRequest) -> UserDto:
        pass