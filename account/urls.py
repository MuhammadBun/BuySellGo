from django.urls import path,include
from . import views
from knox.views import (
    LogoutView,
    LogoutAllView
)
from django_email_verification import urls as email_urls
urlpatterns = [
    path('create-user/', views.CreateUserAPI.as_view(),name='create-user'),
    path('update-user/<int:pk>/', views.UpdateUserAPI.as_view()),
    path('login/', views.LoginAPIView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('logout-all/', LogoutAllView.as_view()),
    path('search_user/', views.search_users,name='search_users'),
    path('search_all/', views.search),
    path('rating/<int:pk>/', views.rate_user,name='rate_user'),
 
     
]
