
from typing import Optional
from pydantic import BaseModel, Field
class Wine(BaseModel):
    fixed_acidity : Optional[float] = Field(0.0, example=7.4)
    volatile_acidity : Optional[float]
    citric_acid : Optional[float]
    residual_sugar : Optional[float]

    chlorides : Optional[float]
    free_sulfur_dioxide : Optional[float]
    total_sulfur_dioxide : Optional[float]
    density : Optional[float]

    pH : Optional[float]
    sulphates : Optional[float]
    alcohol : Optional[float]

class WineLabelised(Wine):
    quality : Optional[int] = Field(...,gt=0,le=10, example=5)
