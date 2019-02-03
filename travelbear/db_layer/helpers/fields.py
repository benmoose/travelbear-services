from uuid import uuid4

from django.db import models


def ExternalIDField():
    return models.UUIDField(default=uuid4, unique=True, db_index=True, editable=False)
