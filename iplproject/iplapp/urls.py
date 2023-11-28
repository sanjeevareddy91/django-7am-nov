from django.urls import path
from .views import welcome_message,sample_page,register,register_franchesis

urlpatterns = [
    path('hello/',welcome_message),
    path('sample/',sample_page,name="sample_page"),
    path('register/',register,name="register"),
    path('register_franchesis/',register_franchesis,name='register_franchesis')
]
