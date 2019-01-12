from django.urls import path

from .views import create_move, delete_move


urlpatterns = [
    path("", create_move.create_move_handler),
    path("<move_id>/", delete_move.delete_move_handler),
]
