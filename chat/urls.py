from django.shortcuts import render

# Create your views here.
from django.urls import path
from . import views
 

urlpatterns = [
         path('create_chat/', views.new_chat,name='new_chat'),
         path('mark_as_read/', views.mark_as_read,name='mark_as_read'),
         path('get_chats/', views.get_chats,name='get_chats'),
 
 ]
