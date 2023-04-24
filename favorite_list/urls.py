from django.urls import path
from . import views
 

urlpatterns = [
         path('create_favorite_list/', views.new_favorite_list,name='new_favorite_list'),
         path('get_favorite_list/', views.get_favorite_lists,name='get_favorite_lists'),
         path('get_favorite_list_items/', views.get_favorite_list_items,name='get_favorite_list_items'),
         path('add_to_favorite_list/', views.add_to_favorite_list,name='add_to_favorite_list'),
         path('update_favorite_list_title/', views.update_favorite_list_title,name='update_favorite_list_title'),
         path('remove_from_favorite_list/', views.remove_from_favorite_list,name='remove_from_favorite_list'),
         path('delete_favorite_list/', views.delete_favorite_list,name='delete_favorite_list'),
 
         
]
