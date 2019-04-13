from uuid import uuid4

from django.db import models

from db_layer.helpers import ModelBase


class User(ModelBase):
    user_id = models.UUIDField(
        default=uuid4, unique=True, db_index=True, editable=False
    )

    external_id = models.CharField(
        max_length=255, null=False, blank=False, unique=True, db_index=True
    )
    email = models.EmailField(blank=True)
    full_name = models.TextField(blank=True)
    short_name = models.TextField(blank=True)
    picture = models.URLField(blank=True)

    is_active = models.BooleanField(default=True)
