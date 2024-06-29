from django import forms
from .models import UnusedExtension, UsedExtension
from django.contrib.auth.forms import AuthenticationForm

class AjouterExtensionUtiliseeForm(forms.ModelForm):
    class Meta:
        model = UsedExtension
        fields = ['name', 'hostname', 'floor', 'position']  # Champs existants et nouveaux champs

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'hostname': forms.TextInput(attrs={'class': 'form-control'}),
            'floor': forms.NumberInput(attrs={'class': 'form-control'}),  # Utilisation de NumberInput pour les champs numériques
            'position': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
class AjouterExtensionNonUtiliseeForm(forms.ModelForm):
    class Meta:
        model = UnusedExtension
        fields = ['name']  # Les champs que vous souhaitez afficher dans le formulaire

class ModifierExtensionNonUtiliseeForm(forms.ModelForm):
    class Meta:
        model = UnusedExtension
        fields = ['name']  # Les champs que vous souhaitez afficher dans le formulaire

class ModifierExtensionUtiliseeForm(forms.ModelForm):
    class Meta:
        model = UsedExtension
        fields = ['name', 'hostname', 'floor', 'position']  # Ajoutez les nouveaux champs ici

        
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom d\'utilisateur'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'}))
    
    
class ExtensionImportForm(forms.Form):
    excel_file = forms.FileField(label='Sélectionnez un fichier Excel')
    
class ExtensionImportForm(forms.Form):
    excel_file = forms.FileField(label='Sélectionnez un fichier Excel')
