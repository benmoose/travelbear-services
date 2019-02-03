from django.db import models

from db_layer.helpers import ModelBase, ExternalIDField
from .trip import Trip


class Location(ModelBase):
    location_id = ExternalIDField()

    trip = models.ForeignKey(Trip, on_delete=models.PROTECT)
    display_name = models.TextField()
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)

    google_place_id = models.CharField(max_length=255, blank=True)

    is_deleted = models.BooleanField(default=False)
