# Generated by Django 3.2.4 on 2021-08-07 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20210807_1812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='encontradoPerdido',
            field=models.CharField(choices=[('perdido', 'PERDIDO'), ('encontrado', 'ENCONTRADO')], default='encontrado', max_length=10),
        ),
    ]
