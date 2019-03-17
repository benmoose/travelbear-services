from random import choices
from string import ascii_letters

from django.db import models

from db_layer.helpers import ModelBase
from db_layer.trip.models import Trip

INVITATION_CODE_LENGTH = 9


def generate_invitation_code():
    """
    >>> import re
    >>> code = generate_invitation_code()
    >>> re.match(r"^[a-zA-Z]{9}$", code) is not None
    True
    """
    code = choices(population=ascii_letters, k=INVITATION_CODE_LENGTH)
    return "".join(code)


class InvitationCode(ModelBase):
    trip = models.ForeignKey(Trip, on_delete=models.PROTECT)
    expiry_date = models.DateTimeField(null=True, blank=True)
    invitation_code = models.CharField(
        max_length=127,
        primary_key=True,
        editable=False,
        default=generate_invitation_code,
    )
