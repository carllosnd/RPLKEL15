# Generated by Django 4.1.7 on 2023-05-22 09:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_rename_stok_terjual_penjualan_stok_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaksi',
            fields=[
                ('idpembayaran', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('nama', models.CharField(max_length=255)),
                ('alamat', models.CharField(max_length=255)),
                ('tglpembayaran', models.DateField()),
                ('totalpembayaran', models.IntegerField()),
                ('metodepembayaran', models.CharField(max_length=255)),
                ('idpemesanan', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.pemesanan')),
            ],
        ),
    ]
