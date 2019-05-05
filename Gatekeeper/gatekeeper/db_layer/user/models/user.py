from django.db import models

from db_layer.model_base import ModelBase


class User(ModelBase):
    user_id = models.CharField(primary_key=True, editable=False, max_length=128)

    full_name = models.TextField(blank=True)
    short_name = models.TextField(blank=True)
    picture = models.URLField(blank=True)

    is_active = models.BooleanField(default=True)
