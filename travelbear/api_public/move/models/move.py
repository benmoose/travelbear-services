from api_public.trips.models import Location
from common.api import api_model
from common.api.validation import required_fields, get_type_mismatch_error_message


@api_model
class Move:
    __slots__ = (
        "start_location_id",
        "end_location_id",
        "start_location",
        "end_location",
    )

    @classmethod
    def from_db_model(cls, db_model):
        return cls(
            start_location=Location.from_db_model(db_model.start_location),
            end_location=Location.from_db_model(db_model.end_location),
        )

    def get_validation_errors(self):
        errors = required_fields(
            self, ["start_location_id", "end_location_id"]
        )
        if not isinstance(self.start_location_id, str):
            errors.append(get_type_mismatch_error_message("start_location_id", str))
        if not isinstance(self.end_location_id, str):
            errors.append(get_type_mismatch_error_message("end_location_id", str))
        return errors
