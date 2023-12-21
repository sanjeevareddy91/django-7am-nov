from django.urls import path
# from .views import welcome_message,sample_page,register,register_franchesis,list_franchesis,update_franchesis,delete_franchesis,register_modelform,register_form,RegisterUser,login_user
from .views import *

urlpatterns = [
    path('hello/',welcome_message),
    path('sample/',sample_page,name="sample_page"),
    path('register/',register,name="register"),
    path('register_franchesis/',register_franchesis,name='register_franchesis'),
    path('list_franchesis/',list_franchesis,name='list_franchesis'),
    path('update/<id>',update_franchesis,name='update_franchesis'),
    path('delete/<id>',delete_franchesis,name='delete_franchesis'),
    path('model_form/',register_modelform,name="register_modelform"),
    path('normal_form/',register_form,name="register_form"),
    path('',RegisterUser,name='register_user'),
    path('login/',login_user,name="login_user"),
    path('logout/',logout_user,name="logout_user"),
    path('forgot_email/',forgot_email,name='forgot_email'),
    path('verify_otp/<id>',verify_otp,name='verify_otp'),
    path('password_change/<id>',password_change,name="password_change"),
    path('schedule/',schedule,name="schedule"),
    path('cls_message/',MessageView.as_view(),name="cls_message"),
    path('cls_register/',SampleFromView.as_view(),name='cls_register'),
    path('cls_registerfranchesis/',RegisterFranchesisView.as_view(),name='cls_registerfranchesis'),
    path('cls_list_franchesis/',ListFranchesisView.as_view(),name='cls_list_franchesis'),
    path('cls_generic_create/',FranchesisGenericCreateView.as_view(),name='cls_generic_create'),
    path('cls_generic_detail/<pk>',FranchesisGenericDetailView.as_view(),name='cls_generic_detail'),
    path('cls_generic_update/<pk>',FranchesisGenericUpdateView.as_view(),name='cls_generic_update'),
    # apis urls
    path('sample_api',sample_api,name="sample_api"),
    path('register_franchesis_api',register_franchesis_api,name="register_franchesis_api"),
    path('update_delete_get_franchesis_api/<id>',update_delete_get_franchesis_api,name="update_delete_get_franchesis_api"),
    path('serializer_register_franchesis_api',serializer_register_franchesis_api,name="serializer_register_franchesis_api"),
    path('update_delete_get_serializer_franchesis_api/<id>',update_delete_get_serializer_franchesis_api,name="update_delete_get_serializer_franchesis_api"),

]
