# Password hashing & JWT logic

import os
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

# Secret Key used to sign JWTs (Read from environment or default for dev)
SECRET_KEY = os.getenv("JWT_SECRET", "super_secret_studentx_key_12345")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """ Hashes a raw password string using bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """ Verifies a plain password against a stored bcrypt hash """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    """ Generates a signed JWT with an expiration timestamp """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)