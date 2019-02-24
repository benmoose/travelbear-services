from common.model import api_model
from common.parse import safe_parse_lat_lng_string


@api_model
class Coords:
    __slots__ = ("lat", "lng")

    @classmethod
    def from_string(cls, lat_lng_string):
        """
        >>> Coords.from_string("51.020202,-0.12239")
        Coords(lat=51.020202, lng=-0.12239)
        >>> Coords.from_string("")
        """
        lat_lng = safe_parse_lat_lng_string(lat_lng_string)
        if lat_lng is None:
            return None

        lat, lng = lat_lng
        return cls(lat=lat, lng=lng)

    def to_tuple(self):
        return self.lat, self.lng


def test_coords_to_tuple():
    assert Coords().to_tuple() == (None, None)
    assert Coords(51, -0.12).to_tuple() == (51, -0.12)
    assert Coords(lat=51, lng=-0.12).to_tuple() == (51, -0.12)
    assert Coords(lat=51).to_tuple() == (51, None)
    assert Coords(lng=-0.12).to_tuple() == (None, -0.12)


def test_coords_from_string():
    assert Coords(51.000001, -0.12) == Coords.from_string("51.000001,-0.12")
    assert Coords(51.000001, 1.0) == Coords.from_string("51.0000005,1")
    assert Coords.from_string("91,181") is None
    assert Coords.from_string("foo") is None
