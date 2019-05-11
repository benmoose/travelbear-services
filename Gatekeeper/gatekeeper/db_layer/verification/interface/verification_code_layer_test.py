from datetime import datetime

import pytest
import pytz
from django.db import IntegrityError

from ..models.verification_code import VerificationCode
from .verification_code_layer import (
    create_verification_code,
    invalidate_verification_code,
)


@pytest.fixture
def expiry_time():
    return datetime(2019, 1, 1, tzinfo=pytz.UTC)


@pytest.mark.django_db
def test_create_verification_code(expiry_time):
    assert 0 == len(VerificationCode.objects.all())
    verification_code = create_verification_code("+447000000000", "abcd", expiry_time)
    assert 1 == len(VerificationCode.objects.all())
    assert "+447000000000" == verification_code.phone_number
    assert "abcd" == verification_code.code
    assert expiry_time == verification_code.expires_at


@pytest.mark.django_db
def test_create_verification_code_unique_codes(expiry_time):
    create_verification_code("+447000000000", "abcd", expiry_time)
    with pytest.raises(IntegrityError):
        create_verification_code("+447000000001", "abcd", expiry_time)


@pytest.mark.django_db
def test_create_verification_code_duplicate_phone_numbers_allowed(expiry_time):
    create_verification_code("+447000000000", "abcd", expiry_time)
    create_verification_code("+447000000000", "abcde", expiry_time)


@pytest.mark.django_db
def test_invalidate_verification_code(expiry_time):
    verification_code = create_verification_code("+447000000000", "abcd", expiry_time)
    assert verification_code.is_active

    invalidate_verification_code(verification_code)
    verification_code.refresh_from_db()
    assert False is verification_code.is_active
