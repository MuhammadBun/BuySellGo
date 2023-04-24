# chat/urls.py
from django.urls import path

from . import views
# chat/routing.py
from django.urls import re_path

from . import consumers






urlpatterns = [
 
    path("create_notification/", views.create_notification, name="create_notification"),
    path("list_notifications/", views.list_notifications , name = "list_notifications"),
    path("mark_as_read/", views.mark_as_read, name = "mark_as_read" ),
    path("delete_notification/", views.delete_notification, name = "delete_notification" ),
    path("get_notification_target/", views.get_notification_target, name = "get_notification_target" ),
]

 