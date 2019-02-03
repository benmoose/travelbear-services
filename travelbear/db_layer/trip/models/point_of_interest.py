from django.db import models

from db_layer.helpers import ModelBase, ExternalIDField
from .location import Location


class PointOfInterest(ModelBase):
    poi_id = ExternalIDField()

    location = models.ForeignKey(Location, on_delete=models.PROTECT)

    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)

    is_booked = models.BooleanField(default=False)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    google_place_id = models.CharField(max_length=255, blank=True)
