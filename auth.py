from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

pwd_context=CryptContext(schemes=["bcrypt"])

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(plain:str , hashed:str):
    return pwd_context.verify(plain,hashed)


SECRET_KEY = "suffyan_secret_key"
ALGORITHM = "HS256"
EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_token(username: str):
    data = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
    }
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")