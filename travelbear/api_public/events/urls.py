from django.urls import path

from .views import create_event


urlpatterns = [path("events/", create_event.create_event, name="create-event")]
