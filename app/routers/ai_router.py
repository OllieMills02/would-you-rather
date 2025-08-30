from fastapi import APIRouter, Response, Depends
from starlette.responses import HTMLResponse

from app.config.model_config import get_model
from train import WyrModelTrainer

router = APIRouter(prefix="/would-you-rather")

@router.get("/train", response_class=HTMLResponse)
def train_model(model: WyrModelTrainer = Depends(get_model)):
    try:
        model.train()
        return Response(content="Model successfully trained", status_code=200)
    except Exception as e:
        return Response(content=f"Model not successfully trained: {e}",status_code=500)

@router.get("/{prompt}", response_class=Response)
def generate_text(prompt: str, model: WyrModelTrainer = Depends(get_model)):
    try:
        generated_text = model.generate_text(prompt)
        return Response(content=generated_text, media_type="text/plain", status_code=200)
    except Exception as e:
        return Response(content=str(e), status_code=500)