from datetime import timedelta, datetime, timezone

from pwdlib.hashers import argon2
from falcon.http_error import HTTPError
from jose import jwt, JWTError
from decouple import config

SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")

passwd = argon2.Argon2Hasher()


def password_match(password: str, password2: str):
    if password != password2:
        raise HTTPError(status=400, description="Both passwords should match")

    return password


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    expires = datetime.now(timezone.utc) + (
        expires_delta if expires_delta else timedelta(minutes=30)
    )

    to_encode.update({"exp": expires, "type": "access"})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    expires = datetime.now(timezone.utc) + (
        expires_delta if expires_delta else timedelta(days=7)
    )

    to_encode.update({"exp": expires, "type": "refresh"})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return encoded_jwt


def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    except JWTError as e:
        print("THIS IS JWT ERROR", e)
