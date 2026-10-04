from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from config import APP_NAME, BASE_DIR, CORS_ORIGINS, GEMINI_API_KEY, GEMINI_MODEL
from db import init_db

from routes.auth_routes import router as auth_router
from routes.page_routes import router as page_router
from routes.planner_routes import router as planner_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=APP_NAME,
    version="1.0.0",
    description="PocketSmart AI - Smart Budget & Recommendation Assistant",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static",
)


app.include_router(page_router)
app.include_router(auth_router)
app.include_router(planner_router)


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "application": APP_NAME,
        "ai_configured": bool(GEMINI_API_KEY),
        "gemini_model": GEMINI_MODEL,
    }


@app.post("/api/startup")
def startup():
    init_db()

    return {
        "status": "initialized"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )