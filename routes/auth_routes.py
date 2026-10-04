from fastapi import (
    APIRouter,
    HTTPException,
    Request,
    Response,
)

from auth import (
    COOKIE_NAME,
    create_access_token,
    get_current_user,
    hash_password,
    verify_password,
)

from db import db_session

from models.schemas import (
    LoginRequest,
    RegisterRequest,
)


router = APIRouter(
    prefix="/api",
    tags=["authentication"],
)


@router.post("/register")
def register(
    payload: RegisterRequest,
    response: Response,
):

    with db_session() as db:

        existing = db.execute(
            """
            SELECT id
            FROM users
            WHERE email = ?
            """,
            (payload.email,),
        ).fetchone()

        if existing:

            raise HTTPException(
                status_code=409,
                detail="An account with that email already exists",
            )

        cursor = db.execute(
            """
            INSERT INTO users
            (
                email,
                password_hash,
                full_name
            )
            VALUES (?, ?, ?)
            """,
            (
                payload.email,
                hash_password(
                    payload.password
                ),
                payload.full_name.strip(),
            ),
        )

        user_id = cursor.lastrowid

    token = create_access_token(
        user_id,
        payload.email,
    )

    response.set_cookie(
        COOKIE_NAME,
        token,
        httponly=True,
        samesite="lax",
        max_age=86400,
    )

    return {

        "message":
            "Registration successful",

        "user": {

            "id":
                user_id,

            "email":
                payload.email,

            "full_name":
                payload.full_name.strip(),
        },
    }


@router.post("/login")
def login(
    payload: LoginRequest,
    response: Response,
):

    email = payload.email.strip().lower()

    with db_session() as db:

        user = db.execute(
            """
            SELECT *
            FROM users
            WHERE email = ?
            """,
            (email,),
        ).fetchone()

    if (
        not user
        or not verify_password(
            payload.password,
            user["password_hash"],
        )
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    token = create_access_token(
        user["id"],
        user["email"],
    )

    response.set_cookie(
        COOKIE_NAME,
        token,
        httponly=True,
        samesite="lax",
        max_age=86400,
    )

    return {

        "message":
            "Login successful",

        "user": {

            "id":
                user["id"],

            "email":
                user["email"],

            "full_name":
                user["full_name"],
        },
    }


@router.post("/logout")
def logout(
    response: Response,
):

    response.delete_cookie(
        COOKIE_NAME
    )

    return {
        "message":
            "Logged out"
    }


@router.post("/token")
def token(
    payload: LoginRequest,
):

    email = payload.email.strip().lower()

    with db_session() as db:

        user = db.execute(
            """
            SELECT *
            FROM users
            WHERE email = ?
            """,
            (email,),
        ).fetchone()

    if (
        not user
        or not verify_password(
            payload.password,
            user["password_hash"],
        )
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
        user["id"],
        user["email"],
    )

    return {

        "access_token":
            access_token,

        "token_type":
            "bearer",
    }


@router.get("/session-info")
def session_info(
    request: Request,
):

    user = get_current_user(
        request
    )

    return {

        "authenticated":
            True,

        "user":
            user,
    }


@router.get("/session-data")
def session_data(
    request: Request,
):

    user = get_current_user(
        request
    )

    with db_session() as db:

        total = db.execute(
            """
            SELECT COUNT(*) AS count
            FROM recommendation_history
            WHERE user_id = ?
            """,
            (user["id"],),
        ).fetchone()["count"]

        recent = db.execute(
            """
            SELECT
                id,
                planner_type,
                created_at
            FROM recommendation_history
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT 5
            """,
            (user["id"],),
        ).fetchall()

    return {

        "user":
            user,

        "recommendation_count":
            total,

        "recent":
            [
                dict(item)
                for item in recent
            ],
    }