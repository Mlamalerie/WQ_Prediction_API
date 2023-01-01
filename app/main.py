import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.routers.wines import router as wines_router
from app.routers.models import router as model_router
from app.routers.predictions import router as predicts_router

app = FastAPI(
    title="Wine Quality Predictor",
    description="🌠 API to predict wine quality 🍷. Grâce à cette API, vous pouvez facilement prédire la qualité d'un vin en utilisant les modèles de machine learning les plus performants, tout en ayant la possibilité de les mettre à jour en ajoutant de nouvelles données.",
    version="0.5",
    contact=
    {
        "name": "Mlamali SAID SALIMO",
        "email": "saidsalimo[at]cy-tech.fr",
    }
)

origins = ["http://localhost:8005"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(wines_router)
app.include_router(model_router)
app.include_router(predicts_router)

@app.get("/")
async def root():
    return {"message": "Welcome to my WineApp API",
            "app_contacts": {"name": "Mlamali SAID SALIMO", "email": "saidsalimo[at]cy-tech.fr", "github" : "@Mlamalerie"}}

