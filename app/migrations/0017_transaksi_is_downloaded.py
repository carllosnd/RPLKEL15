# Generated by Django 4.1.7 on 2023-05-26 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_notifikasi'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaksi',
            name='is_downloaded',
            field=models.BooleanField(default=False),
        ),
    ]
