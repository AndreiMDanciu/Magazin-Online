from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Produs)
class ProdusAdmin(admin.ModelAdmin):
    list_display = ('denumire', 'pret')
    search_fields = ('denumire',)
    list_filter = ('pret',)

@admin.register(Comanda)
class ComandaAdmin(admin.ModelAdmin):
    list_display = ('user_username', 'pret_total', 'data_plasare', 'status_comanda', 'platita',)
    search_fields = ('user__username',)
    list_filter = ('pret_total', 'data_plasare', 'status_comanda',)

    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'Username'

@admin.register(ItemComanda)
class ItemComandaAdmin(admin.ModelAdmin):
    list_display = ('comanda', 'produs', 'cantitate')
    list_filter = ('produs',)
