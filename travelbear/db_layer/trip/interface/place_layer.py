from datetime import datetime

from django.db import transaction

from db_layer.helpers import update_object

from ..models import Location, Place


def create_place(
    location: Location,
    display_name: str,
    lat: float,
    lng: float,
    display_address: str = "",
    start_time: datetime = None,
    end_time: datetime = None,
    google_place_id: str = "",
) -> Place:
    return Place.objects.create(
        location=location,
        display_name=display_name,
        lat=lat,
        lng=lng,
        display_address=display_address,
        start_time=start_time,
        end_time=end_time,
        google_place_id=google_place_id,
    )


def delete_place(place: Place) -> Place:
    with transaction.atomic():
        place_to_delete = Place.objects.select_for_update().get(pk=place.pk)
        if place_to_delete.is_deleted:
            return place_to_delete
        place_to_delete.is_deleted = True
        place_to_delete.save(update_fields=["is_deleted", "modified_on"])
        return place_to_delete


def update_place(place: Place, **kwargs):
    updateable_fields = {
        "display_name",
        "description",
        "display_address",
        "lat",
        "lng",
        "start_time",
        "end_time",
        "google_place_id",
    }
    return update_object(place, updateable_fields, **kwargs)
