from datetime import datetime, timedelta
import pytest
import pytz

from db_layer.user import get_or_create_user
from ..models.event import Event
from .event_layer import (
    create_event,
    list_events_for_user,
    list_upcoming_events_for_user,
)


@pytest.fixture
def create_user():
    def _create_user(user_id):
        user, _ = get_or_create_user(user_id, f"{user_id}@test.com")
        return user

    return _create_user


@pytest.mark.django_db
def test_create_event(create_user):
    user = create_user("foo")

    assert 0 == len(Event.objects.all())
    event = create_event(created_by=user, title="test event")
    assert 1 == len(Event.objects.all())

    event_in_db = Event.objects.all()[0]
    assert event == event_in_db
    assert event.created_by == event_in_db.created_by  # only compares pk
    assert event.title == event_in_db.title


@pytest.mark.django_db
def test_list_events_for_user(create_user):
    user_1 = create_user("1")
    someone_else = create_user("2")

    _ = create_event(
        created_by=someone_else, title="other secret event we shouldn't see"
    )

    event_1 = create_event(created_by=user_1, title="event 1")
    event_1.save_with_times(created_on=datetime(2018, 1, 1, tzinfo=pytz.UTC))
    event_2 = create_event(created_by=user_1, title="event 2")
    event_2.save_with_times(created_on=datetime(2018, 1, 2, tzinfo=pytz.UTC))

    events = list_events_for_user(user=user_1)
    assert events == [event_2, event_1]
    events = list_events_for_user(user=user_1, ascending=True)
    assert events == [event_1, event_2]

    event_1.is_deleted = True
    event_1.save()
    assert [event_2] == list_events_for_user(user=user_1)
    assert [event_2, event_1] == list_events_for_user(user=user_1, include_deleted=True)


@pytest.fixture
def test_list_upcoming_events_for_user(create_user):
    time_0 = datetime(2018, 1, 1, tzinfo=pytz.UTC)

    user_1 = create_user("1")
    someone_else = create_user("2")

    _ = create_event(created_by=someone_else, title="...", start_time=time_0)

    _ = create_event(
        created_by=user_1, title=";)", start_time=time_0 - timedelta(hours=2)
    )
    event_now = create_event(created_by=user_1, title=";)", start_time=time_0)
    event_in_future = create_event(
        created_by=user_1, title=";)", start_time=time_0 + timedelta(hours=2)
    )

    assert [event_now, event_in_future] == list_upcoming_events_for_user(
        user=user_1, search_from_time=time_0
    )

    event_in_future.is_deleted = True
    event_in_future.save()
    assert [event_now] == list_upcoming_events_for_user(
        user=user_1, search_from_time=time_0
    )
    assert [event_now, event_in_future] == list_upcoming_events_for_user(
        user=user_1, search_from_time=time_0, include_deleted=True
    )
