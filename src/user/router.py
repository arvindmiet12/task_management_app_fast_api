from fastapi import APIRouter,Depends, Request, status
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.user import controller
from src.user.dtos import UserCreateDTO, UserLoginDTO, UserResponseDTO


user_routes = APIRouter(prefix="/users")

@user_routes.post("/register",response_model=UserResponseDTO, status_code=status.HTTP_201_CREATED)
def register_user(body: UserCreateDTO, db: Session = Depends(get_db)):
    return controller.register(body, db)

@user_routes.post("/login", status_code=status.HTTP_200_OK)
def login_user(body: UserLoginDTO, db: Session = Depends(get_db)):
    return controller.login(body, db)

@user_routes.get("/is_auth", response_model=UserResponseDTO, status_code=status.HTTP_200_OK)
def is_auth(request: Request, db: Session = Depends(get_db)):
    print("request")
    return controller.is_authentication(request, db)





