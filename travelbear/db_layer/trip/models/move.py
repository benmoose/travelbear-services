from uuid import uuid4
from django.db import models

from db_layer.model_base import ModelBase
from db_layer.trip import Location


class Move(ModelBase):
    move_id = models.UUIDField(default=uuid4, unique=True, db_index=True, editable=False)

    from_location = models.OneToOneField(Location, on_delete=models.PROTECT)
    to_location = models.OneToOneField(Location, on_delete=models.PROTECT)

    type = models.CharField(max_length=255, blank=True)
    depart_time = models.DateTimeField(blank=True, null=True)
    arrive_time = models.DateTimeField(blank=True, null=True)
