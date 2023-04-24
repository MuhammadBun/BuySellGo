from django.urls import path
 
from post import views

urlpatterns = [
    path('list_post/', views.post_list,name="post_list"),
    path('new_post/', views.new_post,name='new_post'),
    path('post_pk/<int:pk>/', views.post_pk,name="post_pk"),
    path('get_user_post/', views.get_posts_user,name='get_posts_user'),
    path('search_posts/', views.search_posts,name="search_posts"),
    path('add_like/<int:pk>/', views.add_like,name="add_like"),
    path('remove_like/<int:pk>/', views.remove_like,name="remove_like"),
]               
