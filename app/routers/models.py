from fastapi import APIRouter
from fastapi.responses import FileResponse


from enum import Enum
import os

router = APIRouter(
    prefix="/api/model"
)


class ModelName(str, Enum):
    randomforest = "randomforestregressor.pkl"
    linearregression = "linearregression"


@router.get("/")
async def get_serialized_model(model_name: ModelName = ModelName.randomforest):
    """Get the serialized model
    :param model_name: query parameter for choose the model
    :return:
    """
    path = os.path.join('../../ai/predictors/', model_name)

    if os.path.exists(path):
        return FileResponse(path, media_type="text/plain", filename=model_name)
    else:
        return None


@router.get("/description")
async def get_model_description(model_name: ModelName = ModelName.randomforest) -> dict:
    pass


@router.put("/")  # enrichir le modèle d’une entrée de donnée supplémentaire (un vin en plus)
async def update_model(model_name: ModelName = ModelName.randomforest) -> dict:
    pass


@router.post("/retrain")  # retrain le modèle avec les nouvelles données
async def retrain_model(model_name: ModelName = ModelName.randomforest) -> None:
    pass
