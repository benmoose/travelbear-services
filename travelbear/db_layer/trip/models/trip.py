from uuid import uuid4

from django.db import models
from django.contrib.postgres.fields import JSONField

from db_layer.model_base import ModelBase
from db_layer.user import User


class Trip(ModelBase):
    trip_id = models.UUIDField(
        default=uuid4, unique=True, db_index=True, editable=False
    )

    created_by = models.ForeignKey(User, on_delete=models.PROTECT, db_index=True)
    title = models.TextField()
    description = models.TextField(blank=True)
    tags = JSONField(null=True, blank=True)

    is_deleted = models.BooleanField(default=False)
