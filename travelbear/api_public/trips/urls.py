from django.urls import path

from .views import create_trip, list_trips


def root(request):
    if request.method == "GET":
        return list_trips.list_trips_handler(request)
    if request.method == "POST":
        return create_trip.create_trip_handler(request)


urlpatterns = [path("", root)]
