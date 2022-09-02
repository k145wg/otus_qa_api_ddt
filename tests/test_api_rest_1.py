import pytest
from cerberus import Validator

BASE_URL = "https://dog.ceo/api/"


def test_rest1_1(request_get):
    target = BASE_URL + "breeds/list/all"
    response = request_get(url=target)
    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_rest1_2(request_get):
    target = BASE_URL + "breeds/image/random"
    response = request_get(url=target)
    schema = {
        "message": {"type": "string"},
        "status": {"type": "string"}
    }
    validator = Validator()
    assert response.status_code == 200
    assert validator.validate(response.json(), schema)
    assert response.json()["status"] == "success"


def test_rest1_3(request_get):
    target = BASE_URL + "breed/hound/images"
    response_images = request_get(url=target)
    schema_images = {
        "message": {"type": "list"},
        "status": {"type": "string"}
    }
    validator = Validator()
    target += "/random"
    response_image = request_get(url=target)
    schema_image = {
        "message": {"type": "string"},
        "status": {"type": "string"}
    }
    assert validator.validate(response_images.json(), schema_images)
    assert validator.validate(response_image.json(), schema_image)
    assert response_image.json()["message"] in response_images.json()["message"]


@pytest.mark.parametrize("sub_breed", ["afghan", "basset", "blood", "english", "ibizan", "plott", "walker"])
def test_rest1_4(request_get, sub_breed):
    target = BASE_URL + "breed/hound/" + sub_breed + "/images"
    response_images = request_get(url=target)
    schema_images = {
        "message": {"type": "list"},
        "status": {"type": "string"}
    }
    validator = Validator()
    target += "/random"
    response_image = request_get(url=target)
    schema_image = {
        "message": {"type": "string"},
        "status": {"type": "string"}
    }
    assert validator.validate(response_images.json(), schema_images)
    assert validator.validate(response_image.json(), schema_image)
    assert response_image.json()["message"] in response_images.json()["message"]


@pytest.mark.parametrize("breed", ["affenpinscher", "airedale", "bluetick", "borzoi", "bouvier", "boxer"])
@pytest.mark.parametrize("code, status", [(200, "success")])
def test_rest1_5(request_get, breed, code, status):
    target = BASE_URL + "breed/" + breed + "/images/random"
    response = request_get(url=target)
    assert response.status_code == code
    assert response.json()["status"] == status
