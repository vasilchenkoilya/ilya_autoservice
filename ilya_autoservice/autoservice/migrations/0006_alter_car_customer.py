# Generated by Django 4.2.5 on 2023-09-29 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoservice', '0005_alter_car_plate_alter_car_vin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='customer',
            field=models.CharField(db_index=True, max_length=50, verbose_name='customer'),
        ),
    ]
