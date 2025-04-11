from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages

# Create your views here.

def listare_produse(request):
    produse = Produs.objects.all()
    return render(request, 'magazin_online/lista_produse.html', {'produse': produse})

def detalii_produs(request, produs_id):
    produs = get_object_or_404(Produs, id=produs_id)
    return render(request, 'magazin_online/detalii_produs.html', {'produs': produs})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('lista_produse')
    else:
        form = RegisterForm()
    return render(request, 'magazin_online/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('lista_produse')
        else:
            return render(request, 'magazin_online/login.html', {'form': form})
    else:
        form = LoginForm
    return render(request, 'magazin_online/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('lista_produse')

@login_required
def profil_utilizator(request):
    comenzi = Comanda.objects.filter(user=request.user).exclude(status_comanda='deschisa')
    form = SchimbaParolaForm()

    if request.method == 'POST':
        form = SchimbaParolaForm(request.POST)
        if form.is_valid():
            parola_noua = form.cleaned_data['parola_noua']
            user = request.user
            user.set_password(parola_noua)
            user.save()
            update_session_auth_hash(request, user)  # ca să nu fie delogat
            messages.success(request, "Parola a fost schimbată cu succes.")
            return redirect('profil_utilizator')
    return render(request, 'magazin_online/profil_utilizator.html', {'comenzi': comenzi, 'form':form})

@login_required
def adauga_in_cos(request, produs_id):
    produs = get_object_or_404(Produs, id=produs_id)
    comanda = Comanda.objects.filter(user=request.user, status_comanda='deschisa').first()
    if not comanda:
        comanda=Comanda.objects.create(user=request.user)
    cantitate_selectata = int(request.POST.get('cantitate', 1))
    item_comanda = ItemComanda.objects.filter(comanda=comanda, produs=produs).first()
    if item_comanda:
        item_comanda.cantitate += cantitate_selectata
        item_comanda.save()
    else:
        form = ItemComandaForm(request.POST)
        if form.is_valid():
            item_comanda = form.save(commit=False)
            item_comanda.comanda= comanda
            item_comanda.produs = produs
            item_comanda.save()
            print("Formularul a fost salvat")

    comanda.pret_total = sum(item_comanda.produs.pret * item_comanda.cantitate for item_comanda in comanda.itemcomanda_set.all())
    comanda.save()
    return redirect('cos')

@login_required
def sterge_din_cos(request, produs_id):
    produs = get_object_or_404(Produs, id=produs_id)
    comanda = Comanda.objects.filter(user=request.user, status_comanda='deschisa').first()
    if not comanda:
        return redirect('cos')
    item_comanda = ItemComanda.objects.filter(comanda = comanda, produs = produs).first()
    if item_comanda:
        item_comanda.delete()
        comanda.pret_total = sum(item.produs.pret * item.cantitate for item in comanda.itemcomanda_set.all())
        comanda.save()
    return redirect('cos')

@login_required
def cos(request):
    comanda = Comanda.objects.filter(user=request.user, status_comanda='deschisa').first()
    return render(request, 'magazin_online/cos.html', {'comanda': comanda})

@login_required
def finalizare_comanda(request):
    comanda = Comanda.objects.filter(user=request.user, status_comanda='deschisa').first()

    if not comanda or not comanda.itemcomanda_set.exists():
        return redirect('cos')

    if request.method == 'POST':
        form = FinalizareComandaForm(request.POST, instance=comanda)
        if form.is_valid():
            comanda = form.save(commit=False)
            comanda.pret_total = sum(item.produs.pret * item.cantitate for item in comanda.itemcomanda_set.all())
            comanda.status_comanda = 'plasata'
            comanda.save()
            Comanda.objects.create(user=request.user, status_comanda='deschisa')

            return redirect('detalii_comanda', comanda_id=comanda.id)
    else:
        form = FinalizareComandaForm(instance=comanda)

    return render(request, 'magazin_online/finalizare_comanda.html', {'form': form, 'comanda': comanda})

@login_required
def detalii_comanda(request, comanda_id):
    comanda = get_object_or_404(Comanda, id=comanda_id, user=request.user)
    return render(request, 'magazin_online/detalii_comanda.html', {'comanda': comanda})

@login_required
def plateste_comanda(request, comanda_id):
    comanda = get_object_or_404(Comanda, id=comanda_id, user=request.user)
    comanda.platita = 'Efectuata'
    comanda.save()
    return redirect('lista_produse')
