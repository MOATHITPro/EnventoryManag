# Generated by Django 5.1.1 on 2024-10-08 19:50

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Enventory', '0002_remove_receiving_station_remove_receiving_supplier_and_more'),
        ('Transactions', '0005_alter_receivingreturn_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receivingreturn',
            name='item',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='Enventory.item'),
        ),
        migrations.CreateModel(
            name='DispatchReturn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('return_date', models.DateField(default=django.utils.timezone.now)),
                ('dispatch_date', models.DateField(editable=False)),
                ('document_number', models.CharField(max_length=50, unique=True)),
                ('delivered_by_name', models.CharField(max_length=100)),
                ('delivered_by_id', models.CharField(max_length=50, unique=True)),
                ('received_by_name', models.CharField(max_length=100)),
                ('received_by_id', models.CharField(max_length=50, unique=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('attachments', models.FileField(blank=True, null=True, upload_to='return_attachments/')),
                ('returned_quantity', models.PositiveIntegerField(default=0)),
                ('expected_return_date', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('actual_return_date', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('item_notes', models.TextField(blank=True, null=True)),
                ('beneficiary', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='Enventory.beneficiary')),
                ('dispatch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Transactions.dispatch')),
                ('item', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='Enventory.item')),
                ('warehouse', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='Enventory.warehouse')),
            ],
        ),
    ]
