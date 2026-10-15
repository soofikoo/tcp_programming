import os
from datetime import timedelta, datetime, timezone

import bcrypt
import jwt
from dotenv import load_dotenv


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode(), password_hash.encode())
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHMS = ["HS256"]

def create_access_tokes(user_id: int, role: str) -> str:
    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=60),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])