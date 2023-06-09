# Generated by Django 4.1.7 on 2023-04-20 14:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0010_alter_post_description'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('community', '0002_alter_community_name'),
        ('favorite_list', '0004_rename_post_favoritelist_favorite_post_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favoritelist',
            name='favorite_community',
        ),
        migrations.RemoveField(
            model_name='favoritelist',
            name='favorite_post',
        ),
        migrations.RemoveField(
            model_name='favoritelist',
            name='favorite_user',
        ),
        migrations.AddField(
            model_name='favoritelist',
            name='favorite_communities',
            field=models.ManyToManyField(to='community.community'),
        ),
        migrations.AddField(
            model_name='favoritelist',
            name='favorite_posts',
            field=models.ManyToManyField(to='post.post'),
        ),
        migrations.AddField(
            model_name='favoritelist',
            name='favorite_users',
            field=models.ManyToManyField(related_name='favorited_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
