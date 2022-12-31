from fastapi import APIRouter, Body
from fastapi.responses import FileResponse
from app.src.models.model import ModelName, ModelManager,DatasetManager
from app.src.models.wine import Wine, WineLabelised
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
    model = ModelManager(name=model_name)
    return FileResponse(model.model_path, media_type="application/octet-stream",
                        filename=os.path.basename(model.model_path))


@router.get("/description")
async def get_model_description(model_name: ModelName = ModelName.randomforest) -> dict:
    """Get the description of the model
    :param model_name: query parameter for choose the model
    :return:
    """

    model_manager = ModelManager(name=model_name)

    return {"model_name": model_name, "parameters": model_manager.get_parameters(),
            "metrics": model_manager.get_metrics()}


@router.put("/")  # enrichir le modèle d’une entrée de donnée supplémentaire (un vin en plus)
async def add_wine(wine: WineLabelised) -> dict:
    dataset_manager = DatasetManager()
    wine, wines, is_added = dataset_manager.append_wine(wine=wine)

    if is_added:
        return {"wine_added": wine, "total_wines_record": len(wines), "wines_record": wines}
    else:
        return {"message": "Wine already exists", "total_wines_record": len(wines)}


@router.post("/retrain")  # retrain le modèle avec les nouvelles données
async def retrain_model(model_name: ModelName = ModelName.randomforest) -> None:
    model_manager = ModelManager(name=model_name)
    model_manager.train()
