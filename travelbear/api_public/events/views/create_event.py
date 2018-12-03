from django.views.decorators.http import require_http_methods

from api_public.auth import require_jwt_auth
from common.response import validation_error_response, success_response
from db_layer.event import create_event
from ..models.event import Event


@require_http_methods(["POST"])
@require_jwt_auth
def create_event_handler(request):
    event = get_event_from_request_body(request.POST.dict())
    print(event.validation_errors)
    if not event.is_valid:
        return validation_error_response(validation_errors=event.validation_errors)

    created_event = persist_event(event, created_by=request.user)
    return success_response(status=201, data=created_event)


def get_event_from_request_body(request_body):
    return Event.from_dict(request_body)


def persist_event(event, created_by):
    event = create_event(
        created_by=created_by,
        title=event.title,
        description=event.description,
        start_time=event.start_time,
        end_time=event.end_time,
        max_guests=event.max_guests,
    )
    return Event.from_db_model(event)
