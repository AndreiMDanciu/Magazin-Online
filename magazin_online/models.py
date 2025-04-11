from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Produs(models.Model):
    denumire = models.CharField(max_length=100)
    descriere = models.TextField()
    pret = models.DecimalField(max_digits=10, decimal_places=2)
    imagine = models.ImageField(upload_to='products/')

    class Meta:
        verbose_name_plural = 'Produse'

    def __str__(self):
        return self.denumire

class Comanda(models.Model):

    status_choices = [
        ('deschisa', 'Deschisa'),
        ('plasata', 'Plasata'),
        ('in procesare', 'In procesare'),
        ('expediata', 'Expediata'),
        ('livrata', 'Livrata'),
        ('anulata', 'Anulata'),
    ]

    plata_choices = [
        ('Efectuata', 'Platita'),
        ('Neefectuata', 'Neplatita'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data_plasare = models.DateTimeField(auto_now_add=True)
    pret_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status_comanda = models.CharField(max_length=20, choices=status_choices, default='deschisa')
    platita = models.CharField(max_length=20, choices=plata_choices, default='Neefectuata')
    produse = models.ManyToManyField(Produs, through='ItemComanda')
    adresa_livrare = models.TextField(blank=True, null=True)
    nume_contact = models.CharField(max_length=100, blank=True, null=True)
    telefon_contact = models.CharField(max_length=15, blank=True, null=True)
    metoda_livrare = models.CharField(
        max_length=20,
        choices=[('curier', 'Curier'), ('posta', 'Posta')],
        default='curier'
    )
    metoda_plata = models.CharField(
        max_length=20,
        choices = [('cash', 'Cash la livrare'), ('card', 'Card')],
        default = 'card'
    )

    class Meta:
        verbose_name_plural = 'Comenzi'

    def __str__(self):
        return f'Comanda {self.id} plasata de {self.user.username}'

class ItemComanda(models.Model):
    comanda = models.ForeignKey(Comanda, on_delete=models.CASCADE)
    produs = models.ForeignKey(Produs, on_delete=models.CASCADE)
    cantitate = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name_plural = 'Iteme_Comanda'

    def __str__(self):
        return f'{self.cantitate} x {self.produs.denumire}'
