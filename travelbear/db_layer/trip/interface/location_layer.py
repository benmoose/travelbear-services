from typing import List

from django.db import transaction
from django.db.models import Q

from db_layer.helpers import update_object

from ..models import Location, Place


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
        return _get_user_locations_qs(user=user).get(location_id=location_id)
    except Location.DoesNotExist:
        return None


def get_locations_for_trip(trip):
    return list(Location.objects.filter(trip=trip))


def update_location(location, **kwargs):
    updateable_fields = {"display_name", "lat", "lng", "google_place_id"}
    return update_object(location, updateable_fields, **kwargs)


def get_places_for_location(location: Location, with_times_only=False) -> List[Place]:
    query = Q(is_deleted=False)

    if with_times_only:
        query &= Q(start_time__isnull=False)

    return list(location.place_set.filter(query).order_by("start_time"))


def _get_user_locations_qs(user):
    return Location.objects.filter(trip__created_by=user, is_deleted=False)
