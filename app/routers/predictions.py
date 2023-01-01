from fastapi import APIRouter, Body
from app.src.models.model import ModelName, ModelManager, DatasetManager
from app.src.models.wine import Wine

router = APIRouter(
    prefix="/api/predict", tags=["predict"], responses={404: {"description": "Not found"}}
)


@router.get("/")
async def get_best_wine() -> Wine:
    """Retourne une combinaison de données permettant d'identifier le "vin parfait" (probablement inexistant mais statistiquement possible).

    Returns:
        Wine: un objet Wine contenant les caractéristiques du vin parfait.
    """

    df_wines = DatasetManager().get_base_df_dataset()
    df_wines["quality"] = df_wines["quality"].astype(int)
    df_best_wines = df_wines[df_wines["quality"] >= 7]

    df_best_wines = df_best_wines.drop(["quality", "Id"], axis=1)
    best_wine = {k: round(v, 3) for k, v in df_best_wines.mean().to_dict().items()}

    return {"best_wine": best_wine}


@router.post("/")
async def make_predict(wine: Wine, model_name: ModelName = ModelName.randomforest):
    """Effectue une prédiction de la qualité d'un vin en utilisant un modèle de machine learning spécifié.

   Args:
       wine: un objet Wine contenant les caractéristiques du vin à prédire.
       model_name: le nom du modèle de machine learning à utiliser (random forest par défaut).

   Returns:
       dict: un dictionnaire contenant le nom du modèle utilisé, la prédiction et les caractéristiques du vin.
    """

    model = ModelManager(name=model_name)
    try:
        quality_predicted = model.predict(wine)
    except Exception as e:
        return {"error": str(e)}
    else:
        return {"model_name": model_name, "quality_predicted": 8, "wine": wine}
