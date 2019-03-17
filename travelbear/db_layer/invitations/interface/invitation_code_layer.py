from ..models import InvitationCode


def create_invitation_code(trip, expiry_date=None):
    return InvitationCode.objects.create(trip=trip, expiry_date=expiry_date)


def get_invitation_from_code(invitation_code):
    try:
        return InvitationCode.objects.get(invitation_code=invitation_code)
    except InvitationCode.DoesNotExist:
        return None
