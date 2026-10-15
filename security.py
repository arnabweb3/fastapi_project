import os
from pwdlib import PasswordHash
import jwt
from dotenv import load_dotenv
from datetime import datetime,timedelta,timezone



load_dotenv()


JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
)
if not JWT_SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY is not configured")


password_hash = PasswordHash.recommended()


def hash_password(password:str) -> str:
    return password_hash.hash(password=password)



def verify_password(
        plain_password : str,
        hashed_password : str
) -> bool :

    return password_hash.verify(
        plain_password,
        hashed_password
    )    

def create_access_token(user_id : int) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "exp": expires_at,
    }

    return jwt.encode(
        payload,
        str(JWT_SECRET_KEY),
        algorithm=JWT_ALGORITHM,
    )

