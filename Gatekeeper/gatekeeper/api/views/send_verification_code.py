from django.http import HttpResponse
from django.views.decorators.http import require_POST

from common.response import success_response


@require_POST
def send_verification_code(request) -> HttpResponse:
    return success_response()
