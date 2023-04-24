# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
   re_path(r"ws/notification_user/(?P<room_name>\d+)/$",  consumers.NotificationUserConsumer.as_asgi()),
   re_path(r"ws/notification_community/(?P<community_name>\d+)/$", consumers.NotificationCommunityConsumer.as_asgi()),
   re_path(r"ws/notification_admin/(?P<admin_notifiy>\w+)/$", consumers.NotificationAdminConsumer.as_asgi()),
]
