import random

import requests
from app.src.models.wine import WineLabelised, Wine
from app.src.models.model import ModelName

ENDPOINT = "http://127.0.0.1:8000"


def test_can_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200

def test_can_get_serialized_model():
    response = requests.get(f"{ENDPOINT}/api/model")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/octet-stream"
    assert response.headers["Content-Disposition"] == 'attachment; filename="randomforestregressor.pkl"'


    response = requests.get(f"{ENDPOINT}/api/model?model_name={ModelName.linear}")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/octet-stream"
    assert response.headers["Content-Disposition"] == 'attachment; filename="linearregression.pkl"'


def test_can_get_model_description():
    response = requests.get(f"{ENDPOINT}/api/model/description")
    assert response.status_code == 200



def test_can_add_wine():
    # Test with valid input
    wineq = WineLabelised(fixed_acidity=7.4 + random.random(), volatile_acidity=0.7 , citric_acid=0, residual_sugar=1.9, chlorides=0.076, free_sulfur_dioxide=11, total_sulfur_dioxide=34, density=0.9978, pH=3.51, sulphates=0.56, alcohol=9.4, quality=5)

    add_wine_response = requests.put(f"{ENDPOINT}/api/model", json=wineq.dict())
    assert add_wine_response.status_code == 201

    # Test with wine that already exists in the dataset
    add_wine_response = requests.put(f"{ENDPOINT}/api/model", json=wineq.dict())
    assert add_wine_response.status_code == 409

    # Test with unvalid input
    wine = Wine(fixed_acidity=7.4, volatile_acidity=0.7, citric_acid=0, residual_sugar=1.9, chlorides=0.076,
                          free_sulfur_dioxide=11, total_sulfur_dioxide=34, density=0.9978, pH=3.51, sulphates=0.56,
                          alcohol=9.4)
    payload = wine.dict()
    add_wine_response = requests.put(f"{ENDPOINT}/api/model", json=wine.dict())
    assert add_wine_response.status_code != 201






