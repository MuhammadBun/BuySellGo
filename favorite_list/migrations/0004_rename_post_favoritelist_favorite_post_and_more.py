# Generated by Django 4.1.7 on 2023-04-17 16:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('community', '0002_alter_community_name'),
        ('favorite_list', '0003_favoritelist_post_delete_favoritelistitem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='favoritelist',
            old_name='post',
            new_name='favorite_post',
        ),
        migrations.AddField(
            model_name='favoritelist',
            name='favorite_community',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='community.community'),
        ),
        migrations.AddField(
            model_name='favoritelist',
            name='favorite_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='favorited_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
