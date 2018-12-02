import pytest

from .api_model import api_model


@pytest.fixture
def model():
    @api_model
    class Foo:
        __slots__ = ("foo", "bar")

        def get_validation_errors(self):
            errors = []
            if not isinstance(self.foo, int) or not isinstance(self.bar, int):
                errors.append("foo and bar must both be ints")
            elif self.foo + self.bar == 10:
                errors.append("foo and bar cannot sum to 10")
            return errors

    return Foo


def test_api_model_has_expected_fields(model):
    assert "__api_model__" in model.__dict__
    assert "get_validation_errors" in model.__dict__
    assert "is_valid" in model.__dict__

    assert model.__api_model__
    assert callable(model.get_validation_errors)


def test_api_model_to_dict(model):
    assert model(1, 2).to_dict() == {"foo": 1, "bar": 2}
    assert model(1).to_dict() == {"foo": 1}
    assert model(bar=2).to_dict() == {"bar": 2}

    assert model(1).to_dict(keep_empty_fields=True) == {"foo": 1, "bar": None}
    assert model(bar=2).to_dict(keep_empty_fields=True) == {"foo": None, "bar": 2}


def test_api_model_from_dict(model):
    assert model.from_dict({"foo": 1, "bar": 2}).to_dict() == {"foo": 1, "bar": 2}


def test_is_valid(model):
    assert model(1, 2).is_valid
    assert not model(5, 5).is_valid
    assert model(5, 5).validation_errors == ["foo and bar cannot sum to 10"]
