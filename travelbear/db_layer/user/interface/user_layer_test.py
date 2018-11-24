import pytest

from ..models.user import User
from .user_layer import get_or_create_user, ConflictingUser


def assert_rows_in_db(expected=0):
    assert expected == len(User.objects.all())


@pytest.mark.django_db
def test_create_user():
    assert_rows_in_db(0)
    user, created = get_or_create_user(auth0_id="id", email="foo@bar.com")
    assert_rows_in_db(1)
    assert created

    assert User.objects.all()[0] == user


@pytest.mark.django_db
def test_get_user():
    assert_rows_in_db(0)
    user_1, _ = get_or_create_user(
        auth0_id="auth0-id",
        email="test@domain.com",
        full_name="ben hadfield",
        short_name="ben",
        picture="https://foo.com",
    )
    assert_rows_in_db(1)
    user_2, _ = get_or_create_user(auth0_id="auth0-id", email="test@domain.com")
    assert user_1 == user_2  # only checks PK
    assert user_2.full_name == "ben hadfield"
    assert user_2.short_name == "ben"
    assert user_2.picture == "https://foo.com"

    user_3, _ = get_or_create_user(auth0_id="auth0-id-1", email="test@domain.com")
    assert user_3 != user_1
    assert_rows_in_db(2)


@pytest.mark.django_db
def test_integrity_error():
    user_1, _ = get_or_create_user(auth0_id="id-1", email="foo@bar.com")
    with pytest.raises(ConflictingUser):
        get_or_create_user(auth0_id="id-1", email="different@email.com")
