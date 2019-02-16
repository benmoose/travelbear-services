from common.api import api_model
from common.models import Coords


@api_model
class Place:
    __slots__ = (
        "place_id",
        "location_id",
        "display_name",
        "description",
        "display_address",
        "coords",
        "start_time",
        "end_time",
        "google_place_id",
    )

    @classmethod
    def from_db_model(cls, db_model):
        has_location = db_model.lat is not None and db_model.lng is not None
        return cls(
            place_id=db_model.place_id,
            location_id=db_model.location.location_id,
            display_name=db_model.display_name,
            description=db_model.description,
            display_address=db_model.display_address,
            coords=Coords(lat=db_model.lat, lng=db_model.lng) if has_location else None,
            start_time=db_model.start_time,
            end_time=db_model.end_time,
            google_place_id=db_model.google_place_id,
        )
