# Generated by Django 4.2.1 on 2023-06-01 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpage', '0006_alter_usersmodel_is_blocked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersmodel',
            name='is_blocked',
            field=models.BooleanField(default=False),
        ),
    ]
