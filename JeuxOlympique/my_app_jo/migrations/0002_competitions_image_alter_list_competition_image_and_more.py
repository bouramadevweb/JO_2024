# Generated by Django 5.0.3 on 2024-04-16 15:26

import my_app_jo.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app_jo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitions',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=my_app_jo.models.get_competition_image_path),
        ),
        migrations.AlterField(
            model_name='list_competition',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=my_app_jo.models.get_List_competition_image_path),
        ),
        migrations.AlterField(
            model_name='user',
            name='ClefGeneree',
            field=models.CharField(default='960108caed9314cdd9a6c3f26bf71429', max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=12),
        ),
    ]
