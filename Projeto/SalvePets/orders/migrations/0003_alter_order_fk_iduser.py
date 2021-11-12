# Generated by Django 3.2.4 on 2021-11-11 21:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0002_order_fk_iduser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='FK_iduser',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
