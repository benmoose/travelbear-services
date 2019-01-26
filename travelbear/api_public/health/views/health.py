from django.views.decorators.http import require_http_methods

from common.response import success_response


@require_http_methods(["GET"])
def health_handler(_):
    return success_response(status=200, data={
        "status": "ok",
    })
