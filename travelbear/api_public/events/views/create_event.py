from django.views.decorators.http import require_http_methods

from api_public.auth import require_jwt_auth
from common.response import validation_error_response, success_response
from db_layer.event import create_event
from db_layer.user import get_user_by_id
from ..models.event import Event


@require_http_methods(["POST"])
@require_jwt_auth
def create_event(request):
    event = get_event_from_request(request)
    if not event.is_valid:
        return validation_error_response(validation_errors=event.validation_errors)

    db_event = persist_event(event, created_by=request.user)
    response_event = Event.from_db_model(db_event).to_response_dict()

    return success_response(status=201, data=response_event)


def get_event_from_request(request):
    return Event.from_dict(request.POST)


def persist_event(event, created_by):
    user = get_user_by_id(created_by)
    return create_event(
        created_by=user,
        title=event.title,
        description=event.description,
        start_time=event.start_time,
        end_time=event.end_time,
        max_guests=event.max_guests,
    )
