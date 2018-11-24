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
