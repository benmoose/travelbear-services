from django.db import models

from db_layer.helpers import ExternalIDField, ModelBase

from .location import Location


class Place(ModelBase):
    place_id = ExternalIDField()

    location = models.ForeignKey(Location, on_delete=models.PROTECT)

    display_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    display_address = models.TextField(blank=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)
    is_booked = models.BooleanField(default=False)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    google_place_id = models.CharField(max_length=255, blank=True)

    is_deleted = models.BooleanField(default=False)
