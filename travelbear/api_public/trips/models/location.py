from common.model import api_model


@api_model
class Location:
    __slots__ = ("location_id", "display_name", "lat", "lng")
