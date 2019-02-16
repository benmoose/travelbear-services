from django.db import models

from db_layer.helpers import ModelBase
from db_layer.user import User

from .trip import Trip


class TripMember(ModelBase):
    class Meta:
        unique_together = ("trip", "user")

    trip = models.ForeignKey(Trip, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    is_admin = models.BooleanField(default=False)
