from fastapi import FastAPI

from course.juan.fastapi.jwtapi.config.db import Base, engine
from course.juan.fastapi.jwtapi.routers import users, auth

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/oauth", tags=["oauth"])

@app.get("/")
def read_root():
    return {"message": "Hello World"}
