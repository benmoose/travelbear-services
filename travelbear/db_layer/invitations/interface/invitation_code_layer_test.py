import pytest

from common.parse import safe_parse_rfc3339
from db_layer.trip import create_trip
from db_layer.user import get_or_create_user

from ..models import InvitationCode
from .invitation_code_layer import create_invitation_code, get_invitation_from_code


@pytest.fixture
def time():
    return safe_parse_rfc3339("2019-01-01T10:00:00Z")


@pytest.fixture
def user():
    user, _ = get_or_create_user("user-1")
    return user


@pytest.fixture
def trip(user):
    return create_trip(user, "test trip")


@pytest.mark.django_db
def test_create_invitation_code(time, trip):
    assert 0 == len(InvitationCode.objects.all())

    code_1 = create_invitation_code(trip)
    assert 1 == len(InvitationCode.objects.all())
    assert code_1.expiry_date is None
    assert trip == code_1.trip

    # check multiple codes per trip works
    code_2 = create_invitation_code(trip, expiry_date=time)
    assert 2 == len(InvitationCode.objects.all())
    assert time == code_2.expiry_date


@pytest.mark.django_db
def test_get_invitation_by_code(time, trip):
    code = create_invitation_code(trip, expiry_date=time)

    code_in_db = get_invitation_from_code(code.invitation_code)
    assert code.invitation_code == code_in_db.invitation_code
    assert code.expiry_date == code_in_db.expiry_date
    assert code.trip == code_in_db.trip

    assert get_invitation_from_code("NOT A VALID CODE") is None
