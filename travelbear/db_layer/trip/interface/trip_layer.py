from django.db import transaction
from django.db.models import Q

from db_layer.helpers import update_object

from ..helpers.user_trips import user_trips_qs
from ..models import Trip
from .trip_member_layer import add_member_to_trip


def create_trip(created_by, title, description="", tags=None):
    trip = Trip.objects.create(
        created_by=created_by, title=title, description=description, tags=tags
    )
    add_member_to_trip(created_by, trip, is_admin=True)
    return trip


def delete_trip(user, trip) -> bool:
    try:
        with transaction.atomic():
            trip = Trip.objects.select_for_update().get(created_by=user, pk=trip.pk)
            if trip.is_deleted:
                return trip
            trip.is_deleted = True
            trip.save(update_fields=["is_deleted", "modified_on"])
        return True
    except Trip.DoesNotExist:
        return False


def get_trips_created_by_user(user, include_deleted=False, ascending=False):
    query = Q(created_by=user)

    if not include_deleted:
        query &= Q(is_deleted=False)

    return list(
        Trip.objects.filter(query).order_by(
            "created_on" if ascending else "-created_on"
        )
    )


def get_trip_by_id(user, trip_id):
    try:
        return user_trips_qs(user).get(trip_id=trip_id)
    except Trip.DoesNotExist:
        return None


def update_trip(user, trip, **kwargs):
    updateable_fields = {"title", "description", "tags"}
    if trip not in list(user_trips_qs(user)):
        raise PermissionError
    return update_object(trip, updateable_fields, **kwargs)
