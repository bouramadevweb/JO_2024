# Generated by Django 5.0.3 on 2024-04-16 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app_jo', '0004_alter_competitions_image_alter_user_clefgeneree'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='ClefGeneree',
            field=models.CharField(default='78407444aaf5cb6871974799d44b3b8a', max_length=50),
        ),
    ]
