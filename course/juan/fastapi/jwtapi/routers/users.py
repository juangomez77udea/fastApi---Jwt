from typing import List

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends

from course.juan.fastapi.jwtapi.dependencies.di import get_service
from course.juan.fastapi.jwtapi.dependencies.security import get_current_user
from course.juan.fastapi.jwtapi.entities.user import User
from course.juan.fastapi.jwtapi.schemas.user_dto import UserDto
from course.juan.fastapi.jwtapi.schemas.user_request import UserRequest
from course.juan.fastapi.jwtapi.services.user_service import UserService

router = APIRouter()

@router.get('/', response_model=List[UserDto])
def list_users(service: UserService = Depends(get_service),
               current_user = Depends(get_current_user)):
    return service.find_all()

@router.get('/{user_id}', response_model=UserDto)
def get_user(user_id: int, service: UserService = Depends(get_service),
             current_user: User = Depends(get_current_user)):
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Incorrect User ID')
    user = service.find_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User don't exist.")
    return user

@router.post('/', response_model=UserDto, status_code=status.HTTP_201_CREATED)
def create_user(user: UserRequest, service: UserService = Depends(get_service),
                current_user = Depends(get_current_user)):
    try:
        return service.create(user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
