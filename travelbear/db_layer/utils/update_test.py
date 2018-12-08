import pytest

from .update import get_fields_to_update, UpdateNotAllowed


def test_get_fields_to_update():
    assert get_fields_to_update({"foo", "bar"}, {"foo", "bar"}) == {"foo", "bar"}
    assert get_fields_to_update({"foo", "bar"}, {"foo"}) == {"foo"}
    assert get_fields_to_update({"foo", "bar"}, {"foo"}) == {"foo"}
    assert get_fields_to_update({"foo", "bar"}, set()) == set()
    assert get_fields_to_update(set(), set()) == set()
    with pytest.raises(UpdateNotAllowed) as e:
        get_fields_to_update({"foo", "bar"}, {"foo", "baz"})
        assert "{'baz'}" in e

    with pytest.raises(UpdateNotAllowed) as e:
        get_fields_to_update(set(), {"foo", "bar"})
        assert "{'foo', 'bar'}" in e
