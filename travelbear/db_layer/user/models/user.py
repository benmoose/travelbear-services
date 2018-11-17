from django.db import models

from db_layer.model_base import ModelBase


class User(ModelBase):
    auth0_id = models.CharField(max_length=255, null=False, blank=False, unique=True, db_index=True)
    name = models.TextField()
    short_name = models.TextField()
    picture = models.URLField()
