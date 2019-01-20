from uuid import uuid4

from django.db import models

from db_layer.model_base import ModelBase
from db_layer.user import User
from .trip import Trip


class TripMember(ModelBase):
    class Meta:
        unique_together = ("trip", "user")

    trip_member_id = models.UUIDField(
        default=uuid4, unique=True, db_index=True, editable=False
    )
    trip = models.ForeignKey(Trip, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    is_admin = models.BooleanField(default=False)
