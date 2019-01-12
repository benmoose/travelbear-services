from django.db import transaction
from django.db.models import Prefetch

from db_layer.trip import Location, Move
from db_layer.utils import get_fields_to_update


def get_user_locations_qs(user):
    return Location.objects.filter(trip__created_by=user, is_deleted=False)


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


def get_location_by_id(user, location_id):
    try:
        return get_user_locations_qs(user=user).get(location_id=location_id)
    except Location.DoesNotExist:
        return None


def get_moves_starting_at_location(location):
    return list(location.start_location_for.all())


def get_moves_ending_at_location(location):
    return list(location.end_location_for.all())


def update_location(user, location, **kwargs):
    updateable_fields = {"display_name", "lat", "lng", "google_place_id"}
    fields_to_update = get_fields_to_update(updateable_fields, kwargs.keys())
    with transaction.atomic():
        location = Location.objects.select_for_update().get(
            trip__created_by=user, pk=location.pk
        )
        for field in fields_to_update:
            setattr(location, field, kwargs.get(field))
        location.save(update_fields=[*fields_to_update, "modified_on"])
    return location
