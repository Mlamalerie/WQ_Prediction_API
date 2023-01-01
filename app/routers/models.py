from fastapi import APIRouter, Body
from fastapi.responses import FileResponse
from app.src.models.model import ModelName, ModelManager, DatasetManager
from app.src.models.wine import Wine, WineLabelised
from enum import Enum
import os

router = APIRouter(
    prefix="/api/model",
    tags=["model"],
)


@router.get("/")
async def get_serialized_model(model_name: ModelName = ModelName.randomforest):
    """Récupère le modèle sérialisé.

    Args:
        model_name: paramètre de requête pour choisir le modèle.

    Returns:
        FileResponse: une réponse de fichier contenant le modèle sérialisé.
    """
    model = ModelManager(name=model_name)
    return FileResponse(model.model_path, media_type="application/octet-stream",
                        filename=os.path.basename(model.model_path))


@router.get("/description")
async def get_model_description(model_name: ModelName = ModelName.randomforest) -> dict:
    """Récupère la description du modèle (méthode, hyperparamètres, etc.).

    Args:
        model_name: paramètre de requête pour choisir le modèle.

    Returns:
        dict: un dictionnaire contenant le nom du modèle, ses paramètres et ses métriques.
    """

    model_manager = ModelManager(name=model_name)

    return {"model_name": model_name, "parameters": model_manager.get_parameters(),
            "metrics": model_manager.get_metrics()}


@router.put("/")  # (un vin en plus)
async def add_wine(wine: WineLabelised) -> dict:
    """ Enrichir le modèle d’une entrée de donnée supplémentaire en ajoutant un vin au dataset.

        Args:
            wine: un objet WineLabelised contenant les caractéristiques du vin à ajouter.

        Returns:
            dict: un dictionnaire contenant l'objet vin ajouté, le nombre total de vins dans le dataset et la liste de tous les vins présents dans le dataset. Si le vin existe déjà dans le dataset, retourne un dictionnaire contenant un message d'erreur et le nombre total de vins dans le dataset.
        """
    dataset_manager = DatasetManager()
    wine, wines, is_added = dataset_manager.append_wine(wine=wine)

    if is_added:
        return {"wine_added": wine, "total_wines_record": len(wines), "wines_record": wines}
    else:
        return {"message": "Wine already exists", "total_wines_record": len(wines)}


@router.post("/retrain")  # retrain le modèle avec les nouvelles données
async def retrain_model(model_name: ModelName = ModelName.randomforest) -> dict:
    """ Reentraine le modèle avec les nouvelles données.

    Args:
        model_name: choisir le modèle à reentrainer.

    Returns:
        dict: un dictionnaire contenant le nom du modèle, ses paramètres et ses métriques.
    """
    # too : test unit verifier que le model que error": "Invalid model name"
    model_manager = ModelManager(name=model_name)
    try:
        n_train, n_test = model_manager.train(save_model=False)  # to save_model=False to avoid overwriting the model
    except Exception as e:
        return {"error": str(e)}
    else:
        return {"message": "Model retrained", "model_name": model_name,
                "dataset": {"len_trainset": n_train, "len_testset": n_test}, **model_manager.get_metrics()}
