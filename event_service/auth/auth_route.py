"""
Route handler for authentication purposes
"""
import os
import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..models import Token
from . import user_utils


router = APIRouter()


@router.post("/auth", response_model=Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):

    user = user_utils.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = datetime.timedelta(minutes=int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]))
    access_token = user_utils.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}

