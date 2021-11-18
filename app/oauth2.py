from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schema
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth_scheme = OAuth2PasswordBearer

SECRET_KEY = "09d25e094fa63hg66gi78ht544g77mn93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data = dict):
    on_encode = data.copy()
    token_expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    on_encode.update({"exp": token_expire})
    access_token = jwt.encode(on_encode, SECRET_KEY, algorithm=[ALGORITHM])
    return {"access_token": access_token}


def verify_access_token(token : str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id : str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        tokenData = schema.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return tokenData


def get_current_user(token: str =  Depends(oauth_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token(token, credentials_exception)