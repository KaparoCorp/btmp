# Generated by Django 4.2.17 on 2024-12-21 11:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('soko', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='tags',
        ),
    ]
