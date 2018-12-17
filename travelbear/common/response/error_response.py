import logging

from django.http import JsonResponse


logger = logging.getLogger(__name__)


def error_response(status=400, message=None):
    data = {"ok": False}
    if message is not None:
        data.update({"message": message})

    return JsonResponse(data, status=status)


def validation_error_response(status=400, validation_errors=None):
    data = {"ok": False}
    if not isinstance(validation_errors, (list, type(None))):
        logger.warning(
            "Received a %s type argument when returning a validation error response, expected list type",
            type(validation_errors),
        )
    if validation_errors is not None:
        data.update({"validation_errors": validation_errors})

    return JsonResponse(data, status=status)
