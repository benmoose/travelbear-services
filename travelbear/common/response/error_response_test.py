import json
import pytest

from django.http import HttpResponse

from .error_response import error_response


@pytest.mark.parametrize('status,message', (
    (400, None),
    (403, 'Not allowed'),
))
def test_error_response(status, message):
    response = error_response(status=status, message=message)

    expected_response_data = {
        'message': message,
    } if message else None

    assert isinstance(response, HttpResponse)
    assert response.status_code == status
    assert response.content == json.dumps(expected_response_data)
