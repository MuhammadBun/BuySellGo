# Generated by Django 4.1.7 on 2023-04-13 01:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0008_remove_post_images_post_contact_info'),
    ]

    operations = [
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('admin', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='admin_communities', to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(related_name='communities', to=settings.AUTH_USER_MODEL)),
                ('posts', models.ManyToManyField(related_name='communities', to='post.post')),
            ],
        ),
    ]
