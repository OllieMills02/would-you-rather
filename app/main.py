from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config.model_config import model_manager
from app.routers import ai_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    model_manager.load_models()
    yield
    # Clean up the ML models
    model_manager.models.clear()
app = FastAPI(
    title="Would you rather API",
    description="description",
    lifespan=lifespan,
)

app.include_router(ai_router.router)