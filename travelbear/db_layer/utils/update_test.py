import pytest

from .update import get_fields_to_update, UpdateNotAllowed


def test_get_fields_to_update():
    assert get_fields_to_update({"foo", "bar"}, {"foo", "bar"}) == {"foo", "bar"}
    assert get_fields_to_update({"foo", "bar"}, {"foo"}) == {"foo"}
    assert get_fields_to_update({"foo", "bar"}, {"foo"}) == {"foo"}
    assert get_fields_to_update({"foo", "bar"}, set()) == set()
    assert get_fields_to_update(set(), set()) == set()
    with pytest.raises(UpdateNotAllowed):
        get_fields_to_update({"foo", "bar"}, {"foo", "baz"})
        get_fields_to_update(set(), {"foo"})
