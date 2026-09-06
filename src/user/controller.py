from fastapi import APIRouter, HTTPException,status, Request
from fastapi.responses import JSONResponse
from src.user.dtos import UserCreateDTO, UserLoginDTO
from src.user.models import UserModel
from sqlalchemy.orm import Session
from pwdlib import PasswordHash
from src.utils.settings import settings
from datetime import datetime, timedelta
from jwt.exceptions import InvalidTokenError
import jwt


password_hashed = PasswordHash.recommended()

def get_password_hash(password):
    return password_hashed.hash(password)

def verify_password(plain_password, hashed_password):
    return password_hashed.verify(plain_password, hashed_password)


def register(user: UserCreateDTO, db: Session):
    #return {"message": "User registered successfully..."}
    # print("user")
    is_user_exist = db.query(UserModel).filter(UserModel.username == user.username).first()
    print(is_user_exist)
    ##print(user)
    if is_user_exist:
        raise HTTPException(status_code=400, detail="Username already exists")

    is_user_exist = db.query(UserModel).filter(UserModel.email == user.email).first()
    
    if is_user_exist:
        raise HTTPException(status_code=400, detail="User email address already exists")

    hashed_password = get_password_hash(user.password)

    new_user = UserModel(
        name = user.name,
        username = user.username,
        email = user.email,
        hashed_password = hashed_password
    )
    print(new_user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def login(body:UserLoginDTO, db: Session):
    user = db.query(UserModel).filter(UserModel.username == body.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Username is invalid")

    if not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")

    exp_time = datetime.now() + timedelta(seconds=30)

    ## create jwt token

    ##token = jwt.encode({"_id":user.id, "exp": exp_time}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    payload = {
        "_id": user.id,
        "exp": exp_time.timestamp()

        #datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return {"access_token": token, "token_type": "jwt"}

 
## Token send 
def is_authentication(request: Request, db: Session):
   try:
        token = request.headers.get("Authorization")
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing")

        token = token.split(" ")[-1]  # Assuming the token is in the format "Bearer <token>"

        payload = jwt.decode(token, settings.SECRET_KEY,settings.ALGORITHM)
        user_id = payload.get("_id")
        exp_time = int(payload.get("exp"))
     
        current_time = datetime.now().timestamp()
        print("Current Time:", current_time)
        print("exp_time:", exp_time)
        print(exp_time - current_time)

        if current_time > exp_time:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")

        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return user
   except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are Unauthorized to access this resource")