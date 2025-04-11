from django.urls import path

# from magazin_online.urls import urlpatterns
from . import views

urlpatterns = [
    path('', views.listare_produse, name='lista_produse'),
    path('produs/<int:produs_id>/', views.detalii_produs, name='detalii_produs'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profil_utilizator/', views.profil_utilizator, name='profil_utilizator'),
    path('adauga_in_cos/<int:produs_id>', views.adauga_in_cos, name='adauga_in_cos'),
    path('sterge_din_cos/<int:produs_id>', views.sterge_din_cos, name='sterge_din_cos'),
    path('cos/', views.cos, name='cos'),
    path('finalizare_comanda/', views.finalizare_comanda, name='finalizare_comanda'),
    path('detalii_comanda/<int:comanda_id>/', views.detalii_comanda, name='detalii_comanda'),
    path('plateste_comanda/<int:comanda_id>/', views.plateste_comanda, name='plateste_comanda'),
]