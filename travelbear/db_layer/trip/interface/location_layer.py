from db_layer.trip import Location


def create_location(trip, display_name, lat, lng, google_place_id=None):
    return Location.objects.create(
        trip=trip,
        display_name=display_name,
        lat=lat,
        lng=lng,
        google_place_id=google_place_id,
    )
