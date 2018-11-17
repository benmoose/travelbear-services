import logging

from django.http import JsonResponse


logger = logging.getLogger(__name__)


class ResponseError(TypeError):
    pass


def success_response(status=200, data=None):
    try:
        return JsonResponse(data, status=status, safe=False)
    except TypeError as e:
        logger.exception('Attempted to respond with un-serializable data: (type %s) %s', type(data), data)
        raise ResponseError(f'Cannot serialise type \'{type(data)}\'') from e
