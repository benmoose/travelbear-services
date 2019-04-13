from common.api import api_model
from common.api.validation import get_type_mismatch_error_message, required_fields

from .location import Location


@api_model
class Trip:
    __slots__ = ("trip_id", "title", "description", "tags", "locations", "created_on")

    @classmethod
    def from_dict(cls, data):
        data_copy = data.copy()
        data_copy["description"] = data_copy.get("description", "")
        return cls._from_dict(data_copy)

    @classmethod
    def from_db_model_and_locations(cls, db_model, locations):
        trip = cls.from_db_model(db_model)
        trip.locations = [Location.from_db_model(location) for location in locations]
        return trip

    def get_validation_errors(self):
        errors = required_fields(self, ("title",))
        if not isinstance(self.title, str):
            errors.append(get_type_mismatch_error_message("title", [str]))
        if self.description and not isinstance("description", str):
            errors.append(get_type_mismatch_error_message("description", [str]))
        if self.tags and not isinstance(self.tags, list):
            errors.append("tags must be an array of tags")
        return errors
