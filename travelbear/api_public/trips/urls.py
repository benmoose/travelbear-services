from django.urls import path

from .views import get_trip, handlers


urlpatterns = [path("", handlers.index), path("<trip_id>/", get_trip.get_trip_handler)]
