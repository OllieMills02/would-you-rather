from fastapi import APIRouter, Response, Depends
from starlette.responses import HTMLResponse

from app.config.model_config import get_model
from train import WyrModelTrainer

router = APIRouter(prefix="/would-you-rather")

@router.get("/train", response_class=HTMLResponse)
def train_model(model: WyrModelTrainer = Depends(get_model)):
    model.train()
    return Response(status_code=200)

@router.get("/{prompt}", response_class=Response)
def generate_text(prompt: str, model: WyrModelTrainer = Depends(get_model)):
    return Response(content=model.generate_text(prompt), media_type="text/plain")