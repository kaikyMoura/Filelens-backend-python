from datetime import datetime, timedelta
import os
from jose import JWTError, jwt

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Creates a JWT access token.

    Args:
        data (dict): The data to be encoded in the JWT.
        expires_delta (timedelta, optional): The time delta for which the JWT is valid. Defaults to ACCESS_TOKEN_EXPIRE_MINUTES.

    Returns:
        str: The encoded JWT.
    """
    to_encode = data.copy()
    to_encode.update(
        {
            "exp": datetime.now(tz=datetime.timezone.utc)
            + timedelta(minutes=expires_delta)
        }
    )
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
