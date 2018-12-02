from django.urls import path

from .views import create_event, list_events


urlpatterns = [
    path("events/", create_event.create_event, name="create-event"),
    path("events/", list_events.list_events, name="list-event"),
]
