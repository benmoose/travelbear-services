from django.urls import path

from .views import create_event, list_events


def root(request):
    if request.method == "GET":
        return list_events.list_upcoming_events(request)
    if request.method == "POST":
        return create_event.create_event_handler(request)


urlpatterns = [path("events/", root, name="/events")]
