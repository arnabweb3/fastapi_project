from fastapi import APIRouter,status,Depends,HTTPException
from schemas.auth import LoginRequest, TokenResponse
from models.user import User
from sqlalchemy.orm import Session
from sqlalchemy import select
from database import get_db
from security import *

router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)

@router.post('/login', status_code=status.HTTP_200_OK, response_model=TokenResponse)
def login(
    credentials : LoginRequest,
    db : Session = Depends(get_db)
):
    user = db.scalar(
        select(User).where(
            User.email == credentials.email        
        )   
    )

    if user is None or not verify_password(
        credentials.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(user.id)

    return {
        "access_token": token,
        "token_type": "bearer",
    }