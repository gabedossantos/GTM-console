"""Entry point for the JourneyLens FastAPI application."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import router
from .core.config import get_settings
from .database import Base, SessionLocal, db_engine
from .services.seed import load_demo_data

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    with SessionLocal() as session:
        load_demo_data(session, settings)
    yield


app = FastAPI(title=settings.app_name, version=settings.api_version, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure database tables exist
Base.metadata.create_all(bind=db_engine)

# Register API routes
app.include_router(router)


@app.get("/")
def root() -> dict[str, str]:
    """Landing endpoint with basic information."""

    return {"message": "JourneyLens API", "version": settings.api_version}
