# Generated by Django 4.2.1 on 2023-06-01 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpage', '0003_alter_usersmodel_tell'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersmodel',
            name='is_block',
            field=models.BooleanField(default=False),
        ),
    ]
