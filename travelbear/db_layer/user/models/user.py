from django.db import models

from db_layer.model_base import ModelBase


class User(ModelBase):
    auth0_id = models.CharField(
        max_length=255, null=False, blank=False, unique=True, db_index=True
    )
    email = models.EmailField(blank=True)
    full_name = models.TextField(blank=True)
    short_name = models.TextField(blank=True)
    picture = models.URLField(blank=True)
