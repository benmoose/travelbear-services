import json

import pytest
from django.http import HttpResponse

from common.model import api_model

from .success_response import ResponseError, success_response


@pytest.mark.parametrize(
    "status,data", ((200, None), (201, "Created!"), (201, {"ids": [1, 2, 4, 5]}))
)
def test_success_response(status, data):
    response = success_response(status=status, data=data)

    response_data = json.loads(response.content) if data else None

    assert isinstance(response, HttpResponse)
    assert response.status_code == status
    assert response_data == data


def test_un_serializable_success_response():
    with pytest.raises(ResponseError):
        success_response(data=lambda x: x)


def test_serialise_api_model():
    @api_model
    class Foo:
        __slots__ = ("a", "b")

    response = success_response(data=Foo(1, 2))

    response_data = json.loads(response.content)
    assert response_data == {"a": 1, "b": 2}
