# Generated by Django 5.1.1 on 2024-10-08 23:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Enventory', '0002_remove_receiving_station_remove_receiving_supplier_and_more'),
        ('Transactions', '0009_damageoperation'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockTransfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transfer_date', models.DateField()),
                ('reference_number', models.CharField(max_length=50)),
                ('delivered_by_name', models.CharField(max_length=255)),
                ('delivered_by_id', models.CharField(max_length=50)),
                ('received_by_name', models.CharField(max_length=255)),
                ('received_by_id', models.CharField(max_length=50)),
                ('notes', models.TextField(blank=True, null=True)),
                ('attachments', models.FileField(blank=True, null=True, upload_to='transfers/')),
                ('quantity_transferred', models.IntegerField()),
                ('reason', models.TextField(blank=True, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('destination_warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfers_in', to='Enventory.warehouse')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Enventory.item')),
                ('source_warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfers_out', to='Enventory.warehouse')),
            ],
        ),
    ]
