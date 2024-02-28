# Generated by Django 4.2.1 on 2023-06-06 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userpage', '0007_alter_productmodel_product_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productmodel',
            name='product_name',
            field=models.ForeignKey(max_length=25, on_delete=django.db.models.deletion.PROTECT, to='userpage.product'),
        ),
    ]
