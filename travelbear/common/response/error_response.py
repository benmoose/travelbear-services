from django.http import JsonResponse


def error_response(status=400, message=None):
    data = {'error': True}
    if message is not None:
        data.update(message=message)

    return JsonResponse(data, status=status)
