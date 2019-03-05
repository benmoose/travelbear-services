import pytest

from db_layer.user.models import User

from .db import count_models_in_db, no_models_in_db


@pytest.mark.django_db
def test_no_models_in_db():
    assert 0 == len(User.objects.all())

    assert no_models_in_db(User)
    User.objects.create(external_id="foo")
    assert not no_models_in_db(User)


@pytest.mark.django_db
def test_count_models_in_db():
    assert 0 == count_models_in_db(User)
    for i in range(5):
        User.objects.create(external_id=str(i))
        assert i + 1 == count_models_in_db(User)
