# Generated by Django 5.1.1 on 2024-10-14 22:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Enventory', '0006_alter_station_stockitem_alter_station_warehouse'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supplier',
            name='stockitem',
        ),
    ]
