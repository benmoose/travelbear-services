import logging
from typing import Optional

from django.db import transaction

from ..models.user import User

logger = logging.getLogger(__name__)


def get_user_by_user_id(user_id: str) -> Optional[User]:
    try:
        return User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return None


def create_user(user_id, phone_number, full_name="", short_name="", picture=""):
    return User.objects.create(
        user_id=user_id,
        phone_number=phone_number,
        full_name=full_name,
        short_name=short_name,
        picture=picture,
    )


def set_user_as_inactive(user: User):
    with transaction.atomic():
        user = User.objects.select_for_update().get(pk=user.pk)
        if not user.is_active:
            return
        user.is_active = False
        user.save(update_fields=["is_active", "modified_on"])


def set_user_as_active(user: User):
    with transaction.atomic():
        user = User.objects.select_for_update().get(pk=user.pk)
        if user.is_active:
            return
        user.is_active = True
        user.save(update_fields=["is_active", "modified_on"])
