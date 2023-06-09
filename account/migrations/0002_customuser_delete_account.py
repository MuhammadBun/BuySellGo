# Generated by Django 4.1.7 on 2023-03-15 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('picture_profile', models.ImageField(blank=True, null=True, upload_to='profile_pics/')),
                ('gender', models.SmallIntegerField(choices=[(1, 'male'), (2, 'female'), (3, 'other')], default=3, verbose_name='gender')),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
        migrations.DeleteModel(
            name='Account',
        ),
    ]
