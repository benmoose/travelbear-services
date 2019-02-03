from datetime import datetime

from db_layer.trip import Location, Place


def create_place(
    location: Location,
    display_name: str,
    lat: float,
    lng: float,
    display_address: str = "",
    is_booked: bool = False,
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
        is_booked=is_booked,
        start_time=start_time,
        end_time=end_time,
        google_place_id=google_place_id,
    )
