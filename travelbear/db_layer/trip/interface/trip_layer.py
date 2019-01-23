from django.db import transaction
from django.db.models import Q, Prefetch

from db_layer.trip import Trip, TripMember, Location
from db_layer.utils import get_fields_to_update
from .trip_member_layer import add_member_to_trip


def create_trip(created_by, title, description="", tags=None):
    trip = Trip.objects.create(
        created_by=created_by, title=title, description=description, tags=tags
    )
    add_member_to_trip(created_by, trip, is_admin=True)
    return trip


def delete_trip(user, trip):
    try:
        with transaction.atomic():
            trip = Trip.objects.select_for_update().get(created_by=user, pk=trip.pk)
            if trip.is_deleted:
                return trip
            trip.is_deleted = True
            trip.save(update_fields=["is_deleted", "modified_on"])
        return trip
    except Trip.DoesNotExist:
        return None


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
        locations_qs = Location.objects.filter(is_deleted=False)
        return Trip.objects.prefetch_related(
            Prefetch("location_set", queryset=locations_qs, to_attr="locations")
        ).get(created_by=user, trip_id=trip_id)
    except Trip.DoesNotExist:
        return None


def update_trip(user, trip, **kwargs):
    updateable_fields = {"title", "description", "tags"}
    fields_to_update = get_fields_to_update(updateable_fields, kwargs.keys())
    with transaction.atomic():
        trip = Trip.objects.select_for_update().get(created_by=user, pk=trip.pk)
        for field in fields_to_update:
            setattr(trip, field, kwargs.get(field))
        trip.save(update_fields=[*fields_to_update, "modified_on"])
    return trip
