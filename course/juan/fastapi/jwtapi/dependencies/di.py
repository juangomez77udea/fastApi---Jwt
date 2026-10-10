from fastapi import Depends
from sqlalchemy.orm import Session

from course.juan.fastapi.jwtapi.config.db import SessionLocal
from course.juan.fastapi.jwtapi.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from course.juan.fastapi.jwtapi.repositories.user_repository import UserRepository
from course.juan.fastapi.jwtapi.services.UserServiceImpl import UserServiceImpl
from course.juan.fastapi.jwtapi.services.user_service import UserService

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_repository(db: Session = Depends(get_db)) -> UserRepository:
    return SQLAlchemyUserRepository(db)

def get_service(db: Session = Depends(get_db),
                repo: UserRepository = Depends(get_repository)) -> UserService:
    return UserServiceImpl(repo, db)