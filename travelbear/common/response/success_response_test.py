import json
import pytest

from django.http import HttpResponse

from .success_response import success_response, ResponseError


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
