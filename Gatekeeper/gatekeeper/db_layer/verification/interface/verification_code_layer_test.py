import pytest
from django.db import IntegrityError

from ..models.verification_code import VerificationCode
from .verification_code_layer import create_verification_code


@pytest.mark.django_db
def test_create_verification_code():
    assert 0 == len(VerificationCode.objects.all())
    verification_code = create_verification_code("+447000000000", "abcd")
    assert 1 == len(VerificationCode.objects.all())
    assert "+447000000000" == verification_code.phone_number
    assert "abcd" == verification_code.code


@pytest.mark.django_db
def test_create_verification_code_unique_codes():
    create_verification_code("+447000000000", "abcd")
    with pytest.raises(IntegrityError):
        create_verification_code("+447000000001", "abcd")


@pytest.mark.django_db
def test_create_verification_code_duplicate_phone_numbers_allowed():
    create_verification_code("+447000000000", "abcd")
    create_verification_code("+447000000000", "abcde")
