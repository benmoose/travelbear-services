from common.api import api_model
from common.api.validation import get_required_field_error_message, required_fields
from common.models import Coords


@api_model
class Location:
    __slots__ = ("location_id", "display_name", "coords", "google_place_id")

    @classmethod
    def from_dict(cls, data):
        return cls(
            display_name=data.get("display_name"),
            coords=Coords(lat=data.get("lat"), lng=data.get("lng")),
            google_place_id=data.get("google_place_id"),
        )

    @classmethod
    def from_db_model(cls, db_model):
        return cls(
            location_id=db_model.location_id,
            display_name=db_model.display_name,
            coords=Coords(lat=db_model.lat, lng=db_model.lng),
            google_place_id=db_model.google_place_id,
        )

    def to_dict(self):
        dct = self._to_dict()
        if self.coords is not None:
            dct["coords"] = self.coords.to_tuple()
        return dct

    def get_validation_errors(self):
        errors = required_fields(self, ("display_name", "coords"))
        if self.coords is None:
            errors.extend(
                [
                    get_required_field_error_message(field_name="lat"),
                    get_required_field_error_message(field_name="lng"),
                ]
            )
        elif self.coords.lat is None:
            errors.append(get_required_field_error_message("lat"))
        elif self.coords.lng is None:
            errors.append(get_required_field_error_message("lng"))
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
        coords=Coords(lat=51.176044, lng=-0.102215),
        google_place_id="goog123",
    )
    assert expected_model == Location.from_dict(data)


def test_to_dict():
    location = Location(
        display_name="some name", coords=Coords(51.2, -0.12), google_place_id="goog123"
    )
    assert {
        "display_name": "some name",
        "coords": (51.2, -0.12),
        "google_place_id": "goog123",
    } == location.to_dict()
