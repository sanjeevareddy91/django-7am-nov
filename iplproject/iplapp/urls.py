from django.urls import path
from .views import welcome_message,sample_page,register

urlpatterns = [
    path('hello/',welcome_message),
    path('sample/',sample_page,name="sample_page"),
    path('register/',register,name="register")
]
