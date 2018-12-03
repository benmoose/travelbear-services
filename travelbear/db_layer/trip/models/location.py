from uuid import uuid4

from django.db import models

from db_layer.model_base import ModelBase
from .trip import Trip


class Location(ModelBase):
    location_id = models.UUIDField(
        default=uuid4, unique=True, db_index=True, editable=False
    )

    trip = models.OneToOneField(Trip, on_delete=models.PROTECT)
    display_name = models.TextField()
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)

    google_place_id = models.CharField(max_length=255, blank=True)
