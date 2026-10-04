import base64
import hashlib
import hmac
import secrets

from datetime import datetime, timedelta, timezone

import jwt

from fastapi import HTTPException, Request, status

from config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    SECRET_KEY,
)

from db import db_session


ALGORITHM = "HS256"

COOKIE_NAME = "pocketsmart_token"


def hash_password(password: str) -> str:

    salt = secrets.token_bytes(16)

    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        200_000,
    )

    return (
        "pbkdf2_sha256$200000$"
        f"{base64.urlsafe_b64encode(salt).decode()}$"
        f"{base64.urlsafe_b64encode(digest).decode()}"
    )


def verify_password(
    password: str,
    encoded_password: str,
) -> bool:

    try:

        scheme, rounds, salt_b64, digest_b64 = (
            encoded_password.split("$")
        )

        if scheme != "pbkdf2_sha256":
            return False

        salt = base64.urlsafe_b64decode(
            salt_b64.encode()
        )

        expected_digest = base64.urlsafe_b64decode(
            digest_b64.encode()
        )

        actual_digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            int(rounds),
        )

        return hmac.compare_digest(
            actual_digest,
            expected_digest,
        )

    except Exception:

        return False


def create_access_token(
    user_id: int,
    email: str,
) -> str:

    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(user_id),
        "email": email,
        "iat": now,
        "exp": now + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        ),
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def decode_token(token: str):

    try:

        return jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

    except jwt.PyJWTError:

        return None


def get_current_user(request: Request):

    token = request.cookies.get(
        COOKIE_NAME
    )

    if not token:

        authorization = request.headers.get(
            "Authorization",
            "",
        )

        if authorization.lower().startswith(
            "bearer "
        ):

            token = authorization[7:].strip()

    payload = (
        decode_token(token)
        if token
        else None
    )

    if not payload:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )

    try:

        user_id = int(
            payload["sub"]
        )

    except (KeyError, ValueError):

        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token",
        )

    with db_session() as db:

        user = db.execute(
            """
            SELECT
                id,
                email,
                full_name,
                created_at
            FROM users
            WHERE id = ?
            """,
            (user_id,),
        ).fetchone()

    if not user:

        raise HTTPException(
            status_code=401,
            detail="User no longer exists",
        )

    return dict(user)