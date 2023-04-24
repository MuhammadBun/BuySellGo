# Generated by Django 4.1.7 on 2023-03-15 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_alter_customuser_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='contact_info',
            new_name='first_name',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='username',
        ),
        migrations.AddField(
            model_name='customuser',
            name='gender',
            field=models.SmallIntegerField(choices=[(1, 'male'), (2, 'female'), (3, 'other')], default=2),
        ),
        migrations.AddField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
