from django.urls import path

from .views import create_move


urlpatterns = [path("", create_move.create_move_handler)]
