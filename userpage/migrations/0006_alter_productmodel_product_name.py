# Generated by Django 4.2.1 on 2023-06-06 11:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userpage', '0005_unit_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productmodel',
            name='product_name',
            field=models.ForeignKey(max_length=25, on_delete=django.db.models.deletion.PROTECT, to='userpage.product'),
        ),
    ]
