from django.db import transaction
from django.db.models import Q

from ..models.trip import Trip


def create_trip(created_by, title, description="", tags=None):
    return Trip.objects.create(
        created_by=created_by, title=title, description=description, tags=tags
    )


def delete_trip(trip):
    with transaction.atomic():
        trip = Trip.objects.select_for_update().get(pk=trip.pk)
        if trip.is_deleted:
            return trip
        trip.is_deleted = True
        trip.save(update_fields=["is_deleted", "modified_on"])
    return trip


def list_trips_for_user(user, include_deleted=False, ascending=False):
    query = Q(created_by=user)

    if not include_deleted:
        query &= Q(is_deleted=False)

    return list(
        Trip.objects.filter(query).order_by(
            "created_on" if ascending else "-created_on"
        )
    )
