import pytest

from db_layer.user import User

from .update import UpdateNotAllowed, is_update_allowed, update_object


@pytest.fixture
def user():
    return User.objects.create(external_id="test-user")


@pytest.mark.django_db
def test_update_object_happy_case(user):
    updated_user = update_object(user, {"email"}, email="test@travelbear.com")
    assert user == updated_user

    user.refresh_from_db()
    assert user.email == "test@travelbear.com"


@pytest.mark.django_db
def test_update_object_all_fields(user):
    updated_user = update_object(
        user, None, email="test@travelbear.com", is_active=False
    )
    assert user == updated_user

    user.refresh_from_db()
    assert user.email == "test@travelbear.com"
    assert user.is_active is False


@pytest.mark.django_db
def test_update_object_invalid(user):
    with pytest.raises(UpdateNotAllowed):
        update_object(user, {"email"}, email="foo@bar.com", is_deleted=True)


@pytest.mark.django_db
def test_foo(user):
    update_object(user, {"email"})


def test_is_update_allowed():
    assert is_update_allowed({"foo", "bar"}, {"foo", "bar"})
    assert is_update_allowed({"foo", "bar"}, {"foo"})
    assert is_update_allowed({"foo", "bar"}, {"foo"})
    assert is_update_allowed({"foo", "bar"}, set())
    assert is_update_allowed(set(), set())

    assert is_update_allowed({"foo", "bar"}, {"foo", "baz"}) is False
    assert is_update_allowed(set(), {"foo", "bar"}) is False
