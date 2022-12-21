from fastapi import APIRouter, Body
from app.src.models.wine import Wine
router = APIRouter(
    prefix="/api/predict"
)

@router.get("/")
async def get_best_wine() -> Wine:
    pass

@router.post("/")
async def make_predict(body: Wine = Body(...)): #response_model=...
    pass

