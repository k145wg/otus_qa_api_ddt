import pytest
import requests
from jsonschema import validate

BASE_URL = "https://api.openbrewerydb.org/breweries"


@pytest.mark.parametrize("method, code",
                         [("get", 200), ("post", 404), ("put", 404), ("patch", 404), ("delete", 404)])
def test_rest2_1(method, code):
    target = BASE_URL
    response = getattr(requests, method)(url=target)
    assert response.status_code == code


def test_rest2_2(request_get):
    target = BASE_URL
    response = request_get(url=target)
    schema = {
        "properties": {
            "id": {"type": "string"},
            "name": {"type": "string"},
            "brewery_type": {"type": "string"},
            "street": {"type": "string"},
            "city": {"type": "string"},
            "state": {"type": "string"},
            "postal_code": {"type": "string"},
            "country": {"type": "string"},
            "longitude": {"type": "string"},
            "latitude": {"type": "string"},
            "phone": {"type": "string"},
            "updated_at": {"type": "string"},
            "created_at": {"type": "string"}
        },
        "required": ["id", "name", "brewery_type", "street", "address_2", "address_3", "city", "state",
                     "county_province", "postal_code", "country", "longitude", "latitude", "phone", "website_url",
                     "updated_at", "created_at"]
    }
    validate(instance=response.json(), schema=schema)


@pytest.mark.parametrize("param, value",
                         [("by_city", "san_diego"), ("by_dist", "38.8977,77.0365"), ("by_name", "cooper"),
                          ("by_state", "new_york"), ("by_postal", "44107"), ('per_page', "3")])
def test_rest2_3(request_get, param, value):
    target = BASE_URL + "?" + param + "=" + value
    response = request_get(url=target)
    assert response.status_code == 200


@pytest.mark.parametrize("value",
                         ["micro", "nano", "regional", "brewpub", "large", "planning", "bar", "contract", "proprieter",
                          "closed"])
def test_rest2_4(request_get, value):
    target = BASE_URL + "?by_type=" + value
    response = request_get(url=target)
    assert response.status_code == 200


def test_rest2_5(request_get):
    target = BASE_URL + "?by_type=qwety123"
    error_json = {"errors": [
        "Brewery type must include one of these types: [\"micro\", \"nano\", \"regional\", \"brewpub\", \"large\", \"planning\", \"bar\", \"contract\", \"proprieter\", \"closed\"]"]}
    response = request_get(url=target)
    assert response.status_code == 400
    assert response.json() == error_json
