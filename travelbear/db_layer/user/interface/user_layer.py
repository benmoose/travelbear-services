import logging

from django.db import transaction, IntegrityError

from ..models.user import User


logger = logging.getLogger(__name__)


class ConflictingUser(IntegrityError):
    pass


def get_user_by_id(user_id):
    try:
        return User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return None


def get_or_create_user(auth0_id, email, full_name="", short_name="", picture=""):
    try:
        with transaction.atomic():
            return User.objects.get_or_create(
                auth0_id=auth0_id,
                email=email,
                defaults=dict(
                    full_name=full_name, short_name=short_name, picture=picture
                ),
            )
    except IntegrityError as e:
        logger.exception("Attempted to get a user with conflicting details")
        raise ConflictingUser from e
