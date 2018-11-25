from django.views.decorators.http import require_http_methods

from api_public.auth import require_jwt_auth


@require_http_methods(['POST'])
@require_jwt_auth
def create_event():
    pass
