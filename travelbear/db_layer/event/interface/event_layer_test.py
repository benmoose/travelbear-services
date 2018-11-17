import pytest

from db_layer.user import get_or_create_user
from ..models.event import Event
from .event_layer import create_event


@pytest.fixture
def user():
    user, _ = get_or_create_user('id', 'foo@bar.com')
    return user


@pytest.mark.django_db
def test_create_event(user):
    assert 0 == len(Event.objects.all())
    event = create_event(created_by=user, title='test event')
    assert 1 == len(Event.objects.all())

    event_in_db = Event.objects.all()[0]
    assert event == event_in_db
    assert event.created_by == event_in_db.created_by
    assert event.title == event_in_db.title
