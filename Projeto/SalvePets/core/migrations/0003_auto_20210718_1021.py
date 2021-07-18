# Generated by Django 3.2.4 on 2021-07-18 13:21

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20210715_0705'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pet',
            name='comprimento',
        ),
        migrations.RemoveField(
            model_name='pet',
            name='largura',
        ),
        migrations.AlterField(
            model_name='pet',
            name='coordenada',
            field=django.contrib.gis.db.models.fields.PointField(default='POINT(-46.655739771980336 -23.56583057162753)', srid=4326),
        ),
    ]
