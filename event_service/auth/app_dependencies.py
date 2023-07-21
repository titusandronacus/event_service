from typing import Annotated

from fastapi import Depends, HTTPException, status
from jose import JWTError

from . import user_utils
from ..models import TokenData

from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth')


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    auth_ex = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid authentication credentials",
                            headers={"WWW-Authenticate": "Bearer"}
                            )
    try:
        payload = user_utils.decode_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise auth_ex
        token_data = TokenData(username=username)
    except JWTError:
        raise auth_ex
    user = user_utils.get_user(username=token_data.username)
    if user is None:
        raise auth_ex

    return user
