import logging

from django.db import transaction

from ..models.user import User

logger = logging.getLogger(__name__)


def get_user_by_external_id(external_id):
    try:
        return User.objects.get(external_id=external_id)
    except User.DoesNotExist:
        return None


def get_or_create_user(external_id, email="", full_name="", short_name="", picture=""):
    with transaction.atomic():
        return User.objects.get_or_create(
            external_id=external_id,
            defaults=dict(
                email=email, full_name=full_name, short_name=short_name, picture=picture
            ),
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
