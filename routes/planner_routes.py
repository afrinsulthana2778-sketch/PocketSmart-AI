import json

from fastapi import (
    APIRouter,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile,
)

from auth import get_current_user

from config import MAX_UPLOAD_MB

from db import db_session

from models.schemas import (
    HomeRequest,
    PartyRequest,
)

from services.gemini_service import (
    gemini_service,
)


router = APIRouter(
    prefix="/api",
    tags=["planners"],
)


def save_history(
    user_id,
    planner_type,
    input_data,
    result,
):

    with db_session() as db:

        cursor = db.execute(
            """
            INSERT INTO recommendation_history
            (
                user_id,
                planner_type,
                input_json,
                result_json
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                user_id,
                planner_type,
                json.dumps(
                    input_data,
                    ensure_ascii=False,
                ),
                json.dumps(
                    result,
                    ensure_ascii=False,
                ),
            ),
        )

        return cursor.lastrowid


@router.post("/generate-home")
def generate_home(
    payload: HomeRequest,
    request: Request,
):

    user = get_current_user(
        request
    )

    data = payload.model_dump()

    result = gemini_service.generate(
        "home",
        data,
    )

    history_id = save_history(
        user["id"],
        "home",
        data,
        result,
    )

    return {

        "history_id":
            history_id,

        "planner_type":
            "home",

        "result":
            result,
    }


@router.post("/generate-party")
def generate_party(
    payload: PartyRequest,
    request: Request,
):

    user = get_current_user(
        request
    )

    data = payload.model_dump()

    result = gemini_service.generate(
        "party",
        data,
    )

    history_id = save_history(
        user["id"],
        "party",
        data,
        result,
    )

    return {

        "history_id":
            history_id,

        "planner_type":
            "party",

        "result":
            result,
    }


@router.post("/generate-jewelry")
async def generate_jewelry(
    request: Request,

    budget: float = Form(...),

    currency: str = Form("INR"),

    occasion: str = Form(...),

    style: str = Form("Elegant"),

    outfit_description: str = Form(""),

    outfit_image: UploadFile | None = File(None),
):

    user = get_current_user(
        request
    )

    if budget <= 0:

        raise HTTPException(
            status_code=422,
            detail="Budget must be greater than zero",
        )

    image_bytes = None

    mime_type = None

    if (
        outfit_image
        and outfit_image.filename
    ):

        allowed_types = {
            "image/jpeg",
            "image/png",
            "image/webp",
        }

        if outfit_image.content_type not in allowed_types:

            raise HTTPException(
                status_code=400,
                detail="Only JPG, PNG and WebP images are supported",
            )

        image_bytes = (
            await outfit_image.read()
        )

        max_size = (
            MAX_UPLOAD_MB
            * 1024
            * 1024
        )

        if len(image_bytes) > max_size:

            raise HTTPException(
                status_code=413,
                detail=(
                    f"Image must be smaller "
                    f"than {MAX_UPLOAD_MB} MB"
                ),
            )

        mime_type = (
            outfit_image.content_type
        )

    data = {

        "budget":
            budget,

        "currency":
            currency.upper(),

        "occasion":
            occasion,

        "style":
            style,

        "outfit_description":
            outfit_description,

        "image_attached":
            bool(image_bytes),
    }

    result = gemini_service.generate(
        "jewelry",
        data,
        image_bytes=image_bytes,
        mime_type=mime_type,
    )

    history_id = save_history(
        user["id"],
        "jewelry",
        data,
        result,
    )

    return {

        "history_id":
            history_id,

        "planner_type":
            "jewelry",

        "result":
            result,
    }


@router.get("/history")
def history(
    request: Request,
):

    user = get_current_user(
        request
    )

    with db_session() as db:

        rows = db.execute(
            """
            SELECT
                id,
                planner_type,
                input_json,
                result_json,
                created_at
            FROM recommendation_history
            WHERE user_id = ?
            ORDER BY id DESC
            """,
            (user["id"],),
        ).fetchall()

    return {

        "history": [

            {

                "id":
                    row["id"],

                "planner_type":
                    row["planner_type"],

                "input":
                    json.loads(
                        row["input_json"]
                    ),

                "result":
                    json.loads(
                        row["result_json"]
                    ),

                "created_at":
                    row["created_at"],
            }

            for row in rows
        ]
    }


@router.get(
    "/recommendations-details/{history_id}"
)
def recommendation_details(
    history_id: int,
    request: Request,
):

    user = get_current_user(
        request
    )

    with db_session() as db:

        row = db.execute(
            """
            SELECT *
            FROM recommendation_history
            WHERE id = ?
            AND user_id = ?
            """,
            (
                history_id,
                user["id"],
            ),
        ).fetchone()

    if not row:

        raise HTTPException(
            status_code=404,
            detail="Recommendation not found",
        )

    return {

        "id":
            row["id"],

        "planner_type":
            row["planner_type"],

        "input":
            json.loads(
                row["input_json"]
            ),

        "result":
            json.loads(
                row["result_json"]
            ),

        "created_at":
            row["created_at"],
    }