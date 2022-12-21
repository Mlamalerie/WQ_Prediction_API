import requests

ENDPOINT = "http://127.0.0.1:8000"


def test_can_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200

def test_can_get_model():
    response = requests.get(ENDPOINT + "/api/model")
    assert response.status_code == 200

    #response = requests.get(ENDPOINT + "/api/model?model_name=test")
    #assert not response.status_code == 200

def test_can_get_model_description():
    response = requests.get(ENDPOINT + "/api/model/description")
    assert response.status_code == 200

def
    #response = requests.get(ENDPOINT + "/api/model/description?model_name=test")
    #assert not response.status_code == 200

def test_can_add_wine():
    # with valid wine :
    wineq = WineLabelised(fixed_acidity=7.4, volatile_acidity=0.7 , citric_acid=0, residual_sugar=1.9, chlorides=0.076, free_sulfur_dioxide=11, total_sulfur_dioxide=34, density=0.9978, pH=3.51, sulphates=0.56, alcohol=9.4, quality=5)
    payload = wineq.dict()

    add_wine_response = requests.put(ENDPOINT + "/api/model", json=payload)
    assert add_wine_response.status_code == 200

    # with invalid wine :

