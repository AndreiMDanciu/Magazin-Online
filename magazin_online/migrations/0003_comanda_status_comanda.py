# Generated by Django 4.2.20 on 2025-04-10 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magazin_online', '0002_itemcomanda_comanda_produse'),
    ]

    operations = [
        migrations.AddField(
            model_name='comanda',
            name='status_comanda',
            field=models.CharField(choices=[('plasata', 'Plasata'), ('in procesare', 'In procesare'), ('expediata', 'Expediata'), ('livrata', 'Livrata'), ('anulata', 'Anulata')], default='plasata', max_length=20),
        ),
    ]
