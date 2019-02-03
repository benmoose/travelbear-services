from django.db import models

from db_layer.helpers import ModelBase, ExternalIDField
from .location import Location


class Move(ModelBase):
    move_id = ExternalIDField()

    start_location = models.ForeignKey(
        Location, on_delete=models.PROTECT, related_name="start_location_for"
    )
    end_location = models.ForeignKey(
        Location, on_delete=models.PROTECT, related_name="end_location_for"
    )

    travel_method = models.CharField(max_length=255, blank=True)
    depart_time = models.DateTimeField(blank=True, null=True)
    arrive_time = models.DateTimeField(blank=True, null=True)

    is_deleted = models.BooleanField(default=False)
