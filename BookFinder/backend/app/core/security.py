from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from core.config import API_SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/google")

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    **Extract and validate the current user from a JWT token.**

    This function is used as a FastAPI dependency and performs the following steps:

    - **Retrieves** the authentication token via `OAuth2PasswordBearer`.
    - **Decodes and verifies** the JWT using the application's secret key.
    - **Extracts** and returns essential user information from the token payload.

    These checks ensure that each request is authenticated and that the token is both valid and trustworthy.


    Args:
        token (str): JWT token provided via the Authorization header.

    Returns:
        dict (dict): A dictionary containing the user's email and name.

    Raises:
        HTTPException: If the token is missing, invalid, expired, or cannot be decoded.
    """
    try:
        payload = jwt.decode(token, API_SECRET_KEY, algorithms=["HS256"])
        return {"email": payload["sub"], "name": payload.get("name")}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
