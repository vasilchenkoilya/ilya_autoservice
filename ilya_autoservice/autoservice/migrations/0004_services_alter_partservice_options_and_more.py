# Generated by Django 4.2.5 on 2023-10-14 14:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('autoservice', '0003_serviceorder_status_alter_car_plate_alter_car_vin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='name')),
                ('description', tinymce.models.HTMLField(blank=True, default='', max_length=10000, verbose_name='Description')),
                ('image', models.ImageField(blank=True, null=True, upload_to='service_images', verbose_name='image')),
            ],
            options={
                'verbose_name': 'service',
                'verbose_name_plural': 'services',
                'ordering': ['-name'],
            },
        ),
        migrations.AlterModelOptions(
            name='partservice',
            options={'ordering': ['-name'], 'verbose_name': 'part service', 'verbose_name_plural': 'part services'},
        ),
        migrations.AddField(
            model_name='partservice',
            name='part_id',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, verbose_name='part id'),
        ),
        migrations.AddField(
            model_name='serviceorder',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='client'),
        ),
        migrations.AddField(
            model_name='serviceorder',
            name='order_id',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, verbose_name='order id'),
        ),
        migrations.AlterField(
            model_name='car',
            name='customer',
            field=models.CharField(db_index=True, max_length=50, verbose_name='customer'),
        ),
        migrations.AlterField(
            model_name='carmodel',
            name='make',
            field=models.CharField(db_index=True, max_length=100, verbose_name='Brand'),
        ),
        migrations.AlterField(
            model_name='carmodel',
            name='year',
            field=models.IntegerField(db_index=True, verbose_name='year'),
        ),
        migrations.CreateModel(
            name='ServiceReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(db_index=True, max_length=4000, verbose_name='content')),
                ('created_at', models.DateField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_reviewes', to=settings.AUTH_USER_MODEL, verbose_name='reviewer')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='autoservice.services', verbose_name='service')),
            ],
            options={
                'verbose_name': 'service review',
                'verbose_name_plural': 'service reviews',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddField(
            model_name='serviceorder',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='autoservice.services', verbose_name='service'),
        ),
    ]
