from django.views.decorators.http import require_http_methods

from api_public.auth import require_jwt_auth


@require_http_methods(["GET"])
@require_jwt_auth
def list_upcoming_events(request):
    pass
