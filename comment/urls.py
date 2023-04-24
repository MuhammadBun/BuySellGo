from django.urls import path
from . import views
 

urlpatterns = [
         path('create_comment/', views.new_comment , name = "new_comment"),
         path('get_comments_post/<int:post_id>/', views.get_comments, name="get_comments"),
         path('update_comment/<int:comment_id>', views.update_comment, name = "update_comment"),
         path('delete_comment/<int:comment_id>', views.delete_comment, name = "delete_comment"),
         path('get_user_comments/<int:user_id>', views.get_user_comments, name = "get_user_comments"),
 ]
