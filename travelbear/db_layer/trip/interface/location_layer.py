from django.db import transaction
from django.db.models import Prefetch

from db_layer.trip import Location, Move


def create_location(trip, display_name, lat, lng, google_place_id=""):
    return Location.objects.create(
        trip=trip,
        display_name=display_name,
        lat=lat,
        lng=lng,
        google_place_id=google_place_id,
    )


def delete_location(location):
    with transaction.atomic():
        location = Location.objects.select_for_update().get(pk=location.pk)
        if location.is_deleted:
            return location
        location.is_deleted = True
        location.save(update_fields=["is_deleted", "modified_on"])
    return location


def get_location_by_id(location_id):
    try:
        move_qs = Move.objects.filter(is_deleted=False)
        return Location.objects.prefetch_related(
            Prefetch("start_location_for", queryset=move_qs, to_attr="start_for"),
            Prefetch("end_location_for", queryset=move_qs, to_attr="end_for"),
        ).get(location_id=location_id)
    except Location.DoesNotExist:
        return None


def get_moves_starting_at_location(location):
    return list(location.start_location_for.all())


def get_moves_ending_at_location(location):
    return list(location.end_location_for.all())
