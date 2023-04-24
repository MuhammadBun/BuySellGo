from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django_email_verification import urls as email_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('account.urls')),
    path('api/post/', include('post.urls')),
    path('api/favorite_lists/', include('favorite_list.urls')),
    path('api/comments/', include('comment.urls')),
    path('api/chats/', include('chat.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/communities/', include('community.urls')),
    path("api/verification/", include("verify_email.urls")),
    path('email/', include(email_urls), name='email-verification'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
