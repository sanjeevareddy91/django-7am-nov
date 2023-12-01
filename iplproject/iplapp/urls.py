from django.urls import path
from .views import welcome_message,sample_page,register,register_franchesis,list_franchesis,update_franchesis,delete_franchesis,register_modelform,register_form

urlpatterns = [
    path('hello/',welcome_message),
    path('sample/',sample_page,name="sample_page"),
    path('register/',register,name="register"),
    path('register_franchesis/',register_franchesis,name='register_franchesis'),
    path('',list_franchesis,name='list_franchesis'),
    path('update/<id>',update_franchesis,name='update_franchesis'),
    path('delete/<id>',delete_franchesis,name='delete_franchesis'),
    path('model_form/',register_modelform,name="register_modelform"),
    path('normal_form/',register_form,name="register_form"),
]
