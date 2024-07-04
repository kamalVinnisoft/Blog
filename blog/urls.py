from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('',Home,name="home"),
    path('createpost',CreatePost,name="createpost"),
    path('likes/',LikePost,name="likes"),
    path('commentpost/',CommentPost,name="commentpost"),
    path('updatepost/<int:id>/',UpdatePost,name="updatepost"),
    path('deletepost/<int:id>/',DeletePost,name="deletepost"),

]