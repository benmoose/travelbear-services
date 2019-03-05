from common.api import api_model
from common.geo import is_valid_latitude, is_valid_longitude
from common.parse import to_six_dp


@api_model
class Coords:
    __slots__ = ("lat", "lng")

    def __post_init__(self):
        if self.lat is not None:
            lat = to_six_dp(self.lat)
            self.lat = lat if is_valid_latitude(lat) else None
        if self.lng is not None:
            lng = to_six_dp(self.lng)
            self.lng = lng if is_valid_longitude(lng) else None

    def to_tuple(self):
        return self.lat, self.lng

    def serialise(self):
        return self.to_tuple()


def test_initialisation():
    assert Coords("90.1", "180.0") == Coords(90.1, 180)
    assert Coords(90.00000049, 179.9999995) == Coords(90, 180)
    assert Coords("-5.22446688", 0.0000005) == Coords(-5.224467, 0.000001)


def test_to_tuple():
    assert Coords().to_tuple() == (None, None)
    assert Coords(51, -0.12).to_tuple() == (51, -0.12)
    assert Coords(lat=51, lng=-0.12).to_tuple() == (51, -0.12)
    assert Coords(lat=51).to_tuple() == (51, None)
    assert Coords(lng=-0.12).to_tuple() == (None, -0.12)
    assert Coords(91, 10.11).to_tuple() == (None, 10.11)
    assert Coords(91, 190).to_tuple() == (None, None)
