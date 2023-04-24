# Generated by Django 4.1.7 on 2023-03-17 00:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_alter_post_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={},
        ),
        migrations.AlterField(
            model_name='photos',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='post.post'),
        ),
        migrations.AlterUniqueTogether(
            name='photos',
            unique_together={('post',)},
        ),
    ]
