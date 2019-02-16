from django.contrib.postgres.fields import JSONField
from django.db import models

from db_layer.helpers import ExternalIDField, ModelBase
from db_layer.user import User


class Trip(ModelBase):
    trip_id = ExternalIDField()

    created_by = models.ForeignKey(User, on_delete=models.PROTECT, db_index=True)
    title = models.TextField()
    description = models.TextField(blank=True)
    tags = JSONField(null=True, blank=True)

    is_deleted = models.BooleanField(default=False)
