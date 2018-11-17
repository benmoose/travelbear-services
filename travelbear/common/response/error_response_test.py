import json
import pytest

from django.http import HttpResponse

from .error_response import error_response


@pytest.mark.parametrize('status,message', (
    (400, None),
    (403, 'Not allowed'),
    (500, 'Something went wrong on our end...'),
))
def test_error_response(status, message):
    response = error_response(status=status, message=message)

    expected_response_data = {'error': True}
    if message is not None:
        expected_response_data.update({'message': message})

    assert isinstance(response, HttpResponse)
    assert response.status_code == status
    assert json.loads(response.content) == expected_response_data
