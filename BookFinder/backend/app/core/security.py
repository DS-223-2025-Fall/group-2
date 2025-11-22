from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from core.config import API_SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/google")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, API_SECRET_KEY, algorithms=["HS256"])
        return {"email": payload["sub"], "name": payload.get("name")}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")