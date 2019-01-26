from django.urls import include, path


urlpatterns = [
    path("health/", include("api_public.health.urls")),
    path("trips/", include("api_public.trips.urls")),
    path("moves/", include("api_public.move.urls")),
]
