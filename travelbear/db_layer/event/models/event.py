from django.db import models

from db_layer.model_base import ModelBase
from db_layer.user import User


class Event(ModelBase):
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, db_index=True)
    title = models.TextField()
    description = models.TextField(blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    max_guests = models.PositiveIntegerField(null=True, blank=True)

    display_address = models.TextField()
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    approx_display_address = models.TextField()
    approx_lat = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    approx_lng = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )

    protect_real_address = models.BooleanField(default=True)
