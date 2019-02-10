from typing import Any, Optional

from django.db import transaction


class UpdateNotAllowed(AttributeError):
    pass


def update_object(db_model, allowed_fields: Optional[set], **kwargs: Any):
    if not is_update_allowed(allowed_fields, set(kwargs.keys())):
        formatted_fields = ", ".join(kwargs.keys() - allowed_fields)
        raise UpdateNotAllowed(f"Cannot update fields: {formatted_fields}")

    with transaction.atomic():
        model = db_model.__class__.objects.select_for_update().get(pk=db_model.pk)
        for field, value in kwargs.items():
            setattr(model, field, value)
        model.save(update_fields=[*kwargs.keys(), "modified_on"])

    return model


def is_update_allowed(allowed_fields: Optional[set], received_fields: set):
    if allowed_fields is None:
        return True
    # <= means `issubset`
    # dict_keys objects don't provide this as a named method
    return received_fields <= allowed_fields
