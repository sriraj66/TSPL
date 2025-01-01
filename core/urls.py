from core import views
from django.urls import path

urlpatterns = [
    path("",views.index,name='index'),
    path("form",views.register_form,name='register_form'),
    path("login",views.user_login,name='user_login'),
    path("signup",views.user_register,name='user_register'),
    path("logout",views.user_logout,name='user_logout'),
]