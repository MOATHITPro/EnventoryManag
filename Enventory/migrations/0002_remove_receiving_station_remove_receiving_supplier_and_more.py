# Generated by Django 5.1.1 on 2024-09-27 17:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Enventory', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='receiving',
            name='station',
        ),
        migrations.RemoveField(
            model_name='receiving',
            name='supplier',
        ),
        migrations.RemoveField(
            model_name='receiving',
            name='warehouse',
        ),
        migrations.DeleteModel(
            name='ImportedItem',
        ),
        migrations.DeleteModel(
            name='Receiving',
        ),
    ]
