from ..models.trip import Trip
from ..models.trip_member import TripMember


def user_trips_qs(user):
    user_trip_ids = TripMember.objects.filter(
        user=user, trip__is_deleted=False
    ).values_list("trip", flat=True)
    return Trip.objects.filter(id__in=user_trip_ids)
