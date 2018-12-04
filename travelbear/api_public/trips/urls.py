from django.urls import path

from .views import get_trip, create_location, handlers


urlpatterns = [
    path("", handlers.index),
    path("<trip_id>/", get_trip.get_trip_handler),
    path("<trip_id>/locations/", create_location.create_location_handler),
]
