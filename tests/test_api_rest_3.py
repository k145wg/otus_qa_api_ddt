import pytest
import requests
from jsonschema import validate

BASE_URL = "https://jsonplaceholder.typicode.com/"


@pytest.mark.parametrize("method, code",
                         [("get", 200), ("post", 201), ("put", 404), ("patch", 404), ("delete", 404)])
def test_rest3_1(method, code):
    target = BASE_URL + "posts"
    response = getattr(requests, method)(url=target)
    assert response.status_code == code


@pytest.mark.parametrize("method, code",
                         [("get", 200), ("post", 404), ("put", 200), ("patch", 200), ("delete", 200)])
def test_rest3_2(method, code):
    target = BASE_URL + "posts/1"
    response = getattr(requests, method)(url=target)
    assert response.status_code == code


@pytest.mark.parametrize("sub_target", ["/posts/1/comments", "comments?postId=1"])
@pytest.mark.parametrize("method, code",
                         [("get", 200), ("post", 201), ("put", 404), ("patch", 404), ("delete", 404)])
def test_rest3_3(sub_target, method, code):
    target = BASE_URL + "posts/1/comments"
    response = getattr(requests, method)(url=target)
    assert response.status_code == code


def test_rest3_4(request_get):
    target = BASE_URL + "albums"
    response = request_get(url=target)
    schema = {
        "properties": {
            "id": {"type": "number"},
            "userId": {"type": "number"},
            "title": {"type": "string"},
        },
        "required": ["id", "userId", "title"]
    }

    validate(instance=response.json(), schema=schema)


def test_rest3_5(request_get):
    target = BASE_URL + "posts"
    response = request_get(url=target)
    schema = {
        "properties": {
            "id": {"type": "number"},
            "userId": {"type": "number"},
            "title": {"type": "string"},
            "body": {"type": "boolean"}
        },
        "required": ["id", "userId", "title", "body"]
    }
    validate(instance=response.json(), schema=schema)
