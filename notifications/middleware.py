from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from knox.auth import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
User = get_user_model()
from django.contrib.auth.models import AnonymousUser
from account.models import CustomUser
class KnoxAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        
        if scope['type'] == 'websocket':
 
            # Get the token from the query string
            query_params = dict((x.split('=') for x in scope['query_string'].decode().split("&")))
            token = query_params.get('token')
 
            # Authenticate the user using Knox authentication
 
            try:
                user, auth_token = await database_sync_to_async(TokenAuthentication().authenticate_credentials)(token.encode())
                scope['user'] = query_params.get('user_id')
 
            except (AuthenticationFailed, ValueError):
 
                scope['user'] = None
        else:
            # Authenticate the user using JWT authentication (for HTTP requests)
            jwt_auth = JWTAuthentication()
            try:
                user, jwt_token = jwt_auth.authenticate(scope['request'])
                scope['user'] = user
            except (AuthenticationFailed, ValueError):
                scope['user'] = AnonymousUser()

        return await self.inner(scope, receive, send)






 