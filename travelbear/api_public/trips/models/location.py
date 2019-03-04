from common.api import api_model, validation
from common.models import Coords


@api_model
class Location:
    __slots__ = ("location_id", "display_name", "location", "google_place_id")

    @classmethod
    def from_dict(cls, data):
        return cls(
            display_name=data.get("display_name"),
            location=Coords(lat=data.get("lat"), lng=data.get("lng")),
            google_place_id=data.get("google_place_id"),
        )

    @classmethod
    def from_db_model(cls, db_model):
        return cls(
            location_id=db_model.location_id,
            display_name=db_model.display_name,
            location=Coords(lat=db_model.lat, lng=db_model.lng),
            google_place_id=db_model.google_place_id,
        )

    def get_validation_errors(self):
        errors = validation.required_fields(self, ("display_name", "lat", "lng"))
        errors += validation.of_type(self, ("display_name",), str)
        return errors


def test_from_dict():
    data = {
        "display_name": "some name",
        "lat": 51.176044,
        "lng": -0.102215,
        "google_place_id": "goog123",
    }
    expected_model = Location(
        display_name="some name",
        location=Coords(lat=51.176044, lng=-0.102215),
        google_place_id="goog123",
    )
    assert expected_model == Location.from_dict(data)
