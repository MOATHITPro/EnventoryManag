# Generated by Django 5.1.1 on 2024-10-14 22:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Enventory', '0008_remove_beneficiary_stockitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='station',
            name='stockitem',
        ),
    ]
