import pytest

from ..models.user import User
from .user_layer import get_or_create_user, set_user_as_active, set_user_as_inactive


def assert_rows_in_db(expected=0):
    assert expected == len(User.objects.all())


@pytest.mark.django_db
def test_get_or_create_user():
    assert_rows_in_db(0)
    user_1, _ = get_or_create_user(
        user_id="auth0-id",
        full_name="ben hadfield",
        short_name="ben",
        picture="https://foo.com",
    )
    assert_rows_in_db(1)
    user_2, _ = get_or_create_user(user_id="auth0-id")
    assert user_1 == user_2  # only checks PK
    assert user_2.full_name == "ben hadfield"
    assert user_2.short_name == "ben"
    assert user_2.picture == "https://foo.com"

    user_3, _ = get_or_create_user(user_id="auth0-id-1")
    assert user_3 != user_1
    assert_rows_in_db(2)


@pytest.mark.django_db
def test_set_user_as_inactive():
    user, _ = get_or_create_user("foo")

    assert user.is_active
    set_user_as_inactive(user)
    user.refresh_from_db()
    assert not user.is_active

    # check idempotency
    set_user_as_inactive(user)
    user.refresh_from_db()
    assert not user.is_active


@pytest.mark.django_db
def test_set_user_as_active():
    user, _ = get_or_create_user("foo")
    user.is_active = False
    user.save()

    assert not user.is_active
    set_user_as_active(user)
    user.refresh_from_db()
    assert user.is_active

    # check idempotency
    set_user_as_active(user)
    user.refresh_from_db()
    assert user.is_active
