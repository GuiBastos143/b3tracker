# Generated by Django 5.2.1 on 2025-05-19 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0003_asset_tunnel_input_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='tracking_frequency',
            field=models.IntegerField(default=5, help_text='Frequency (minutes)'),
        ),
    ]
