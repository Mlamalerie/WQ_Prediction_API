from fastapi import APIRouter
from app.src.models.wine import Wine, WineLabelised
from app.src.models.model import DatasetManager
from typing import Union

router = APIRouter(
    prefix="/api/wines", tags=["wines"], responses={404: {"description": "Not found"}}
)


@router.get("/")
async def read_wines() -> list:
    """Read wines from csv datasource
    Returns:
        list: wines from datasource
    """
    return DatasetManager().get_base_wines()


@router.post("/")
async def create_wine(wine: Wine) -> dict:
    """Create wine and append it to csv datasource
    Args:
        wine (Wine): wine to append
    Returns:
        dict: wine created
    """
    pass


@router.get("/{id}")
async def read_wine(id: int) -> Union[Wine, None]:
    """Read wine by id
    Args:
        id (int): wine id
    Returns:
        Union[Wine, None]: wine found
    """

    if id < 0 or id >= len(DatasetManager().get_base_wines()):
        return None

    return DatasetManager().get_wine_by_id(id)



@router.delete("/{id}")
async def delete_wine(id: int) -> dict:
    pass