from django.urls import path

from .views import create_location, handlers, itinerary, update_location

urlpatterns = [
    path("", handlers.root_endpoint),
    path("<trip_id>/", handlers.trip_id_endpoint),
    path("<trip_id>/itinerary/", itinerary.itinerary_handler),
    path("<trip_id>/locations/", create_location.create_location_handler),
    path("<trip_id>/locations/<location_id>", update_location.update_location_handler),
]
