# Generated by Django 4.1.7 on 2023-04-23 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_customuser_is_email_verified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_email_verified',
        ),
    ]
