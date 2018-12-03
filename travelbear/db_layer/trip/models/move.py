from uuid import uuid4
from django.db import models

from db_layer.model_base import ModelBase
from .location import Location


class Move(ModelBase):
    move_id = models.UUIDField(
        default=uuid4, unique=True, db_index=True, editable=False
    )

    from_location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name="start_location")
    to_location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name="end_location")

    type = models.CharField(max_length=255, blank=True)
    depart_time = models.DateTimeField(blank=True, null=True)
    arrive_time = models.DateTimeField(blank=True, null=True)
