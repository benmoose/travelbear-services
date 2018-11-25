import attr
import pytest

from .api_model import APIModel


@pytest.fixture
def model():
    @attr.s
    class Foo(APIModel):
        foo = attr.ib(type=int)
        bar = attr.ib(type=int)

        def get_validation_errors(self):
            errors = []
            if self.foo + self.bar != 10:
                errors.append("foo and bar must sum to 10")
            return errors

    return Foo


def test_api_model_validation(model):
    m_invalid = model(foo=1, bar=1)
    assert m_invalid.is_valid is False
    assert m_invalid.validation_errors == ["foo and bar must sum to 10"]

    m_valid = model(foo=5, bar=5)
    assert m_valid.is_valid
    assert m_valid.validation_errors == []
