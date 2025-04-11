from django import forms
from .models import ItemComanda, Comanda
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class ItemComandaForm(forms.ModelForm):
    class Meta:
        model = ItemComanda
        fields = ['produs', 'cantitate']

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class FinalizareComandaForm(forms.ModelForm):
    class Meta:
        model = Comanda
        fields = ['nume_contact', 'telefon_contact', 'adresa_livrare', 'metoda_livrare', 'metoda_plata']

class SchimbaParolaForm(forms.Form):
    parola_noua = forms.CharField(widget=forms.PasswordInput, label="Parolă nouă")
    confirma_parola = forms.CharField(widget=forms.PasswordInput, label="Confirmă parola")

    def clean(self):
        cleaned_data = super().clean()
        parola_noua = cleaned_data.get('parola_noua')
        confirma_parola = cleaned_data.get('confirma_parola')

        if parola_noua != confirma_parola:
            raise forms.ValidationError("Parolele nu coincid.")
        return cleaned_data