from common.model import api_model, validation


@api_model
class Location:
    __slots__ = ("location_id", "display_name", "lat", "lng", "google_place_id")

    def get_validation_errors(self):
        errors = validation.required_fields(self, ("display_name", "lat", "lng"))
        errors += validation.of_type(self, ("display_name",), str)
        errors += validation.of_type(self, ("lat", "lng"), float)
        return errors
