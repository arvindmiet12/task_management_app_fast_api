from datetime import datetime
from pydantic import BaseModel

class UserCreateDTO(BaseModel):
    name: str
    username: str
    password: str
    email: str

class UserResponseDTO(BaseModel):
    id: int
    name: str
    username: str
    email: str


class UserLoginDTO(BaseModel):
    username: str
    password: str

class GetAllUsersDTO(BaseModel):
    name: str
    username: str
    email: str
    created_at: datetime
    updated_at: datetime