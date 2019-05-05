from django.urls import path

from .views import send_verification_code

urlpatterns = [
    path("send-verification-code/", send_verification_code.send_verification_code)
]
