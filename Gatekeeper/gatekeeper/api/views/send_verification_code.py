from typing import Optional
from django.http import HttpResponse
from django.views.decorators.http import require_POST

from common.response import success_response, error_response
from common.model import data_model


@data_model
class RequestData:
    phone_number: str


@require_POST
def send_verification_code(request) -> HttpResponse:
    request_data = get_request_data(request.POST)
    if request_data is None:
        return error_response()

    return success_response({"phone_number": request_data.phone_number})


def get_request_data(request_body: dict) -> Optional[RequestData]:
    try:
        return RequestData.from_dict(request_body)
    except TypeError:
        return None
