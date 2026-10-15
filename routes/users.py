from fastapi import APIRouter,status, Depends,HTTPException
from models.user import User
from schemas.user import UserCreate, UserResponse
from database import get_db
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import select
from security import hash_password



router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.post('/register', status_code= status.HTTP_201_CREATED , response_model=UserResponse)
def register_user(user_data : UserCreate, db : Session = Depends(get_db)):

    existing_user = db.scalar(
        select(User).where(User.email == user_data.email)
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already registered with this email id"
        )

    user = User(
        email = str(user_data.email),
        hashed_password = hash_password(user_data.password)
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already registered with this email id"
        )
    
    except Exception:
        db.rollback()
        raise


    


