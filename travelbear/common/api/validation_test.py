import pytest

from .api_model import api_model
from .validation import of_type


@pytest.fixture
def model():
    @api_model
    class Foo:
        __slots__ = ("a", "b")

    return Foo


def test_of_type(model):

    model_1 = model(a=5, b=1)
    assert of_type(model_1, [], int) == []
    assert of_type(model_1, ["a", "b"], int) == []

    model_2 = model(a="foo", b=True)
    assert of_type(model_2, ["b"], bool) == []
    assert "'a' must be of type bool" in of_type(model_2, ["a", "b"], bool)
