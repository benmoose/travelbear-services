from ..models import VerificationCode


def create_verification_code(phone_number: str, code: str) -> VerificationCode:
    return VerificationCode.objects.create(phone_number=phone_number, code=code)
