from django import forms
from .models import UnusedExtension, UsedExtension
from django.contrib.auth.forms import AuthenticationForm

class AjouterExtensionNonUtiliseeForm(forms.ModelForm):
    class Meta:
        model = UnusedExtension
        fields = ['name']  # Les champs que vous souhaitez afficher dans le formulaire

class ModifierExtensionNonUtiliseeForm(forms.ModelForm):
    class Meta:
        model = UnusedExtension
        fields = ['name']  # Les champs que vous souhaitez afficher dans le formulaire

class AjouterExtensionUtiliseeForm(forms.ModelForm):
    class Meta:
        model = UsedExtension
        fields = ['name']  # Les champs que vous souhaitez afficher dans le formulaire

class ModifierExtensionUtiliseeForm(forms.ModelForm):
    class Meta:
        model = UsedExtension
        fields = ['name']  # Les champs que vous souhaitez afficher dans le formulaire
        
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom d\'utilisateur'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'}))
    
    
class ExtensionImportForm(forms.Form):
    excel_file = forms.FileField(label='Sélectionnez un fichier Excel')
    
class ExtensionImportForm(forms.Form):
    excel_file = forms.FileField(label='Sélectionnez un fichier Excel')
