from django.db.models import Q

from ..models.event import Event


def create_event(
    created_by,
    title,
    description="",
    start_time=None,
    end_time=None,
    max_guests=None,
    display_address="",
    lat=None,
    lng=None,
    approx_display_address="",
    approx_lat=None,
    approx_lng=None,
    protect_real_address=True,
):
    return Event.objects.create(
        created_by=created_by,
        title=title,
        description=description,
        start_time=start_time,
        end_time=end_time,
        max_guests=max_guests,
        display_address=display_address,
        lat=lat,
        lng=lng,
        approx_display_address=approx_display_address,
        approx_lat=approx_lat,
        approx_lng=approx_lng,
        protect_real_address=protect_real_address,
    )


def list_upcoming_events_for_user(user, search_from_time, include_deleted=False):
    query = Q(start_time__gte=search_from_time)

    if not include_deleted:
        query &= Q(is_deleted=False)

    return list(Event.objects.filter(query).order_by("start_time"))


def list_events_for_user(user, include_deleted=False, ascending=False):
    query = Q(created_by=user)

    if not include_deleted:
        query &= Q(is_deleted=False)

    return list(
        Event.objects.filter(query).order_by(
            "created_on" if ascending else "-created_on"
        )
    )
