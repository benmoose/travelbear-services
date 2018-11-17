from django.http import JsonResponse


def error_response(status=400, message=None):
    data = None
    if message is not None:
        data = dict(message=message)
    return JsonResponse(data, status=status)
