from django.contrib import admin
from post.models import Post, Photos

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass

@admin.register(Photos)
class PhotosAdmin(admin.ModelAdmin):
    pass