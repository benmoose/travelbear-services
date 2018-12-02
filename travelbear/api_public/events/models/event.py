from common.model import api_model
from common.parse import safe_parse_rfc_3339


@api_model
class Event:
    __slots__ = ("title", "description", "start_time", "end_time", "max_guests")

    @classmethod
    def from_dict(cls, data):
        max_guests = data.get("max_guests")
        return cls(
            title=data.get("title"),
            description=data.get("description"),
            start_time=safe_parse_rfc_3339(data.get("start_time")),
            end_time=safe_parse_rfc_3339(data.get("end_time")),
            max_guests=int(max_guests) if max_guests else None,
        )

    def get_validation_errors(self):
        errors = []
        required_fields = ("title", "start_time", "end_time")
        for field in required_fields:
            value = getattr(self, field)
            if value is None:
                errors.append(f"{field} is required")
        if isinstance(self.max_guests, int) and self.max_guests < 0:
            errors.append("max_guests must be a positive integer")
        return errors
