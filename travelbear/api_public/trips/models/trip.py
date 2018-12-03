from common.model import api_model
from common.request import validation

from .location import Location


@api_model
class Trip:
    __slots__ = ("trip_id", "title", "description", "tags", "is_deleted", "locations")

    @classmethod
    def from_dict(cls, data):
        data["description"] = data.get("description", "")
        return cls._from_dict(data)

    def __post_init__(self):
        if self.locations:
            self.locations = [
                Location.from_db_model(location) for location in self.locations
            ]

    def get_validation_errors(self):
        errors = validation.required_fields(self, ("title",))
        errors += validation.of_type(self, ("title", "description"), str)
        if self.tags and not isinstance(self.tags, list):
            errors.append("tags must be an array of tags")
        return errors
