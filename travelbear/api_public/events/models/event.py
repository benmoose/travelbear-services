from common.model import api_model
from common.parse import safe_parse_rfc_3339


@api_model
class Event:
    __slots__ = (
        "title",
        "description",
        "start_time",
        "end_time",
        "max_guests",
        "display_address",
        "lat",
        "lng",
        "approx_display_address",
        "approx_lat",
        "approx_lng",
        "protect_real_address",
        "is_deleted",
    )

    @classmethod
    def from_dict(cls, data):
        print('b', data)
        data["max_guests"] = safe_parse_int(data.get("max_guests"))
        data["start_time"] = safe_parse_rfc_3339(data.get("start_time"))
        data["end_time"] = safe_parse_rfc_3339(data.get("end_time"))
        print('a', data)
        return cls._from_dict(data)

    def get_validation_errors(self):
        errors = []
        required_fields = ("title", "start_time", "end_time")
        for field in required_fields:
            value = getattr(self, field)
            if value is None:
                errors.append(f"{field} is required")
        if not isinstance(self.max_guests, int):
            errors.append("max_guests must be an integer")
        elif self.max_guests < 0:
            errors.append("max_guests must be a positive integer")
        return errors


def safe_parse_int(str_value):
    """
    >>> safe_parse_int("50")
    50
    >>> safe_parse_int("50.7")
    51
    >>> safe_parse_int("abc") is None
    True
    """
    try:
        return int(round(float(str_value)))
    except (ValueError, TypeError):
        return None
