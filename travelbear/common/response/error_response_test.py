import json
import pytest

from django.http import HttpResponse

from .error_response import error_response, validation_error_response


@pytest.mark.parametrize(
    "status,message",
    ((400, None), (403, "Not allowed"), (500, "Something went wrong on our end...")),
)
def test_error_response(status, message):
    response = error_response(status=status, message=message)

    expected_response_data = {"ok": False}
    if message is not None:
        expected_response_data.update({"message": message})

    assert isinstance(response, HttpResponse)
    assert response.status_code == status
    assert json.loads(response.content) == expected_response_data


@pytest.mark.parametrize(
    "validation_errors",
    ((None), (["foo is a required field", "bar must be a positive number"])),
)
def test_validation_error_response(validation_errors):
    response = validation_error_response(validation_errors=validation_errors)

    expected_response_data = {"ok": False}
    if validation_errors is not None:
        expected_response_data.update({"validation_errors": validation_errors})

    assert isinstance(response, HttpResponse)
    assert response.status_code == 400
    assert json.loads(response.content) == expected_response_data
