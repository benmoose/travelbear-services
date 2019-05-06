import pytest

from .model import data_model


@pytest.fixture
def data_model_class():
    @data_model
    class Foo:
        x: str
        y: float = 9.42

    return Foo


def test_type_check(data_model_class):
    data_model_class("abc")
    data_model_class("abc", 10.1)
    data_model_class("abc", y=10.1)
    data_model_class(x="abc", y=10.1)

    with pytest.raises(TypeError):
        data_model_class()

    with pytest.raises(TypeError):
        data_model_class(50)

    with pytest.raises(TypeError):
        data_model_class(50, 10.1)

    with pytest.raises(TypeError):
        data_model_class("abc", y="def")


def test_from_dict(data_model_class):
    model = data_model_class.from_dict({"x": "abc", "y": 10.1})
    assert "abc" == model.x
    assert 10.1 == model.y

    model = data_model_class.from_dict({"x": "abc"})
    assert "abc" == model.x
    assert 9.42 == model.y

    with pytest.raises(TypeError):
        data_model_class.from_dict({"y": 10.1})
