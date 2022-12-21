from fastapi import APIRouter
from fastapi.responses import FileResponse
from app.src.models.model import ModelName, ModelManager

from enum import Enum
import os

router = APIRouter(
    prefix="/api/model"
)


@router.get("/")
async def get_serialized_model(model_name: ModelName = ModelName.randomforest):
    """Get the serialized model
    :param model_name: query parameter for choose the model
    :return:
    """
    match model_name:
        case ModelName.randomforest:
            filename = "randomforestregressor.pkl"
        case ModelName.linear:
            filename = "linearregression.pkl"

    path = os.path.join('./app/datasource/predictors/', filename)
    if os.path.exists(path):
        print(model_name)
        return FileResponse(path, media_type="text/plain", filename=filename)
    else:
        return path  # todo : HTPPException


@router.get("/description")
async def get_model_description(model_name: ModelName = ModelName.randomforest) -> dict:
    match model_name:
        case ModelName.randomforest:
            model_filename = "randomforestregressor.pkl"
            metrics_filename = "metrics_rf.json"
        case ModelName.linear:
            model_filename = "linearregression.pkl"
            metrics_filename = "metrics_rf.json"

    model_manager = ModelManager(name=model_name, model_path=f"./app/datasource/predictors/{model_filename}",
                           data_path="./app/datasource/datasets/Wines.csv", metrics_path=f"./app/datasource/predictors/{metrics_filename}")

    return {"model_name": model_name, "parameters": model_manager.get_parameters(), "metrics": model_manager.get_metrics()}


@router.put("/")  # enrichir le modèle d’une entrée de donnée supplémentaire (un vin en plus)
async def update_model(model_name: ModelName = ModelName.randomforest) -> dict:
    pass


@router.post("/retrain")  # retrain le modèle avec les nouvelles données
async def retrain_model(model_name: ModelName = ModelName.randomforest) -> None:
    pass
