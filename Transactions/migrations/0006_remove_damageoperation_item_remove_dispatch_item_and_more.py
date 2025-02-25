# Generated by Django 5.1.1 on 2024-10-15 21:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Enventory', '0012_remove_beneficiary_item_and_more'),
        ('Transactions', '0005_remove_dispatch_stock_item_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='damageoperation',
            name='item',
        ),
        migrations.RemoveField(
            model_name='dispatch',
            name='item',
        ),
        migrations.RemoveField(
            model_name='dispatchreturn',
            name='item',
        ),
        migrations.RemoveField(
            model_name='receiving',
            name='item',
        ),
        migrations.RemoveField(
            model_name='receivingreturn',
            name='item',
        ),
        migrations.RemoveField(
            model_name='transferitem',
            name='item',
        ),
        migrations.AddField(
            model_name='damageoperation',
            name='stock_item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Enventory.stockitem'),
        ),
        migrations.AddField(
            model_name='dispatch',
            name='stock_item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Enventory.stockitem'),
        ),
        migrations.AddField(
            model_name='dispatchreturn',
            name='stock_item',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='Enventory.stockitem'),
        ),
        migrations.AddField(
            model_name='receiving',
            name='stock_item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Enventory.stockitem'),
        ),
        migrations.AddField(
            model_name='receivingreturn',
            name='stock_item',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='Enventory.stockitem'),
        ),
        migrations.AddField(
            model_name='transferitem',
            name='stock_item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Enventory.stockitem'),
        ),
        migrations.AlterField(
            model_name='receiving',
            name='document_number',
            field=models.CharField(blank=True, max_length=50, unique=True),
        ),
    ]
