# Generated by Django 5.0.3 on 2024-04-08 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app_jo', '0002_alter_billet_clefutilisateur_alter_user_clefgeneree'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billet',
            name='ClefUtilisateur',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='ClefGeneree',
            field=models.CharField(default='951cf72d8613104b7fe38ae43200cf76', max_length=50),
        ),
    ]
