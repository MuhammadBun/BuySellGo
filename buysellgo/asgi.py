"""
ASGI config for simplechatapp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

 

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
 
from notifications.routing import websocket_urlpatterns
from notifications.middleware import KnoxAuthMiddleware
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
 

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": KnoxAuthMiddleware(
 
     URLRouter(
            websocket_urlpatterns
        )
 
    ),
})