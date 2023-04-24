from django.urls import path
from . import views
 

urlpatterns = [
         path('get_all_communities/', views.get_communities,name="get_communities"),
         path('get_community/<int:pk>/', views.get_community,name="get_community"),
         path('new_community/', views.new_community,name="new_community"),
         path('join_member_to_community/', views.join_member_to_community,name="join_member_to_community"),
         path('create_post_for_community/', views.create_post_for_community,name="create_post"),
         path('delete_post_for_community/<int:community_id>/post/<int:post_id>/', views.delete_post_for_community,name="delete_post"),
         path('remove_member/<int:community_id>/member/<int:user_id>/', views.remove_member,name="remove_member"),
         path('delete_community/<int:community_id>/', views.delete_community,name="delete_community"),
         path('update_community/<int:pk>/', views.update_community,name="update_community"),
         path('search_communities/', views.search_communities,name="search_communities"),
]
