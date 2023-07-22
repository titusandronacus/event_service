"""
Lookup utils for users (currently only env admin user) utils are here
"""
import os
from datetime import datetime, timedelta

from passlib.context import CryptContext
from jose import jwt

from ..models import User


# admin user provided by env vars
admin_user_dict = {os.environ["ADMIN_USER"]: {"username": os.environ["ADMIN_USER"],
                                              "hashed_password": os.environ["ADMIN_PASS"]
                                              }
                   }

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(username: str):
    if username in admin_user_dict:
        return User(**admin_user_dict[username])


def verify_password(plaintext_pass, hashed_password):
    return pwd_context.verify(plaintext_pass, hashed_password)


def get_hashed_password(password):
    return pwd_context.hash(password)


def decode_token(token) :
    return jwt.decode(token, os.environ["SECRET_KEY"], algorithms=[os.environ["ALGORITHM"]])


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.environ["SECRET_KEY"], algorithm=os.environ["ALGORITHM"])
    return encoded_jwt
