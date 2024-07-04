from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('',SignUp,name="signup"),
    path('signin',SignIn,name="signin"),
    path('users_listing/',users_listing,name="users_listing")
]