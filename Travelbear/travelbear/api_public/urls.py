from django.urls import include, path

urlpatterns = [
    path("trips/", include("api_public.trips.urls")),
    path("moves/", include("api_public.move.urls")),
]
