from django.db import models

from db_layer.model_base import ModelBase


class VerificationCode(ModelBase):
    phone_number = models.CharField(max_length=32, db_index=True)
    code = models.CharField(max_length=32, unique=True)
