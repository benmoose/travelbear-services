from datetime import datetime

from django.db import transaction

from ..models import VerificationCode


def create_verification_code(
    phone_number: str, code: str, expiry_time: datetime
) -> VerificationCode:
    return VerificationCode.objects.create(
        phone_number=phone_number, code=code, expires_at=expiry_time
    )


@transaction.atomic
def invalidate_verification_code(verification_code: VerificationCode):
    _verification_code = VerificationCode.objects.select_for_update().get(
        pk=verification_code.pk
    )
    _verification_code.is_active = False
    _verification_code.save(update_fields=["is_active", "modified_on"])
