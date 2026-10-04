from fastapi import (
    APIRouter,
    Request,
)

from fastapi.responses import (
    HTMLResponse,
    RedirectResponse,
)

from fastapi.templating import (
    Jinja2Templates,
)

from auth import (
    COOKIE_NAME,
    decode_token,
)

from config import BASE_DIR

from db import db_session


router = APIRouter()


templates = Jinja2Templates(
    directory=str(
        BASE_DIR / "templates"
    )
)


def current_user(request: Request):

    token = request.cookies.get(
        COOKIE_NAME
    )

    payload = (
        decode_token(token)
        if token
        else None
    )

    if not payload:

        return None

    try:

        user_id = int(
            payload["sub"]
        )

    except (
        KeyError,
        ValueError,
    ):

        return None

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

    return (
        dict(user)
        if user
        else None
    )


@router.get(
    "/",
    response_class=HTMLResponse,
)
def home(request: Request):

    return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={
        "request": request,
    }
)


@router.get(
    "/login",
    response_class=HTMLResponse,
)
def login_page(
    request: Request,
):

   return templates.TemplateResponse(
    request,
    "login.html",
    {
        "request": request,
    
    }
)



@router.get(
    "/register",
    response_class=HTMLResponse,
)
def register_page(
    request: Request,
):

    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={
            "request": request,
        },
    )


@router.get(
    "/dashboard",
    response_class=HTMLResponse,
)
def dashboard(
    request: Request,
):

    user = current_user(
        request
    )

    if not user:

        return RedirectResponse(
            "/login"
        )

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "request": request,
            "user": user,
        },
    )


@router.get(
    "/history",
    response_class=HTMLResponse,
)
def history_page(
    request: Request,
):

    user = current_user(
        request
    )

    if not user:

        return RedirectResponse(
            "/login"
        )

    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={
            "request": request,
            "user": user,
        },
    )


@router.get(
    "/planner/home",
    response_class=HTMLResponse,
)
def home_planner(
    request: Request,
):

    user = current_user(
        request
    )

    if not user:

        return RedirectResponse(
            "/login"
        )

    return templates.TemplateResponse(
        request=request,
        name="home_planner.html",
        context={
            "request": request,
            "user": user,
        },
    )

@router.get(
    "/planner/party",
    response_class=HTMLResponse,
)
def party_planner(
    request: Request,
):

    user = current_user(
        request
    )

    if not user:

        return RedirectResponse(
            "/login"
        )

    return templates.TemplateResponse(
        request=request,
        name="party_planner.html",
        context={
            "request": request,
            "user": user,
        },
    )

@router.get(
    "/planner/jewelry",
    response_class=HTMLResponse,
)
def jewelry_planner(
    request: Request,
):

    user = current_user(
        request
    )

    if not user:

        return RedirectResponse(
            "/login"
        )

    return templates.TemplateResponse(
        request=request,
        name="jewelry_planner.html",
        context={
            "request": request,
            "user": user,
        },
    )