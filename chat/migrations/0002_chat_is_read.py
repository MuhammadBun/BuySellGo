# Generated by Django 4.1.7 on 2023-04-17 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]
