from pyexpat.errors import messages
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db import IntegrityError , transaction
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .forms import AjouterExtensionNonUtiliseeForm, AjouterExtensionUtiliseeForm, AjouterExtensionUtiliseeForm, ExtensionImportForm, ModifierExtensionNonUtiliseeForm, ModifierExtensionUtiliseeForm, CustomAuthenticationForm, ExtensionImportForm
from .models import Department, UsedExtension, UnusedExtension
from django.db.models import Count
from django.db.models import Q
import pandas as pd
from django.views.decorators.csrf import csrf_protect
from openpyxl import Workbook
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render




def home(request):
    if request.user.is_authenticated:
        return redirect('extend')  # Rediriger vers la vue dashboard si l'utilisateur est déjà connecté
    return render(request, 'accueil/index.html')


def charts(request):
    return render(request, 'dashboard/charts.html')

def erreur(request):
    return render(request, 'dashboard/404.html')

def dashboard(request):
    departments = Department.objects.annotate(
        used_extension_count=Count('used_extensions'),
        unused_extension_count=Count('unused_extensions')
    )
    return render(request, 'extend/extension.html', {'departments': departments})

def extension_utilisees(request, department_id):
    department = Department.objects.get(id=department_id)
    used_extensions = department.used_extensions.all()

    search_query = request.GET.get('search')
    if search_query:
        used_extensions = used_extensions.filter(
            Q(name__icontains=search_query) |
            Q(hostname__icontains=search_query) |
            Q(floor__icontains=search_query) |
            Q(position__icontains=search_query)
        )

    used_extensions = used_extensions.order_by('id')
    
    paginator = Paginator(used_extensions, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'departement/extension_utilisees.html', {'department': department, 'page_obj': page_obj})

def extension_non_utilisees(request, department_id):
    department = Department.objects.get(id=department_id)
    unused_extensions = department.unused_extensions.all()

    search_query = request.GET.get('search')
    if search_query:
        unused_extensions = unused_extensions.filter(name__icontains=search_query)

    unused_extensions =  unused_extensions.order_by('id')
   
    paginator = Paginator(unused_extensions, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'departement/extension_non_utilisees.html', {'department': department, 'page_obj': page_obj})

def ajouter_extension_non_utilisee(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    
    if request.method == 'POST':
        form = AjouterExtensionNonUtiliseeForm(request.POST)
        if form.is_valid():
            extension_non_utilisee = form.save(commit=False)
            extension_non_utilisee.department = department
            
            # Vérifier si l'extension existe déjà parmi les extensions non utilisées pour ce département
            existing_extension = UnusedExtension.objects.filter(name=extension_non_utilisee.name, department=department).exists()
            
            if existing_extension:
                messages.error(request, "Cette extension existe déjà dans les extensions non utilisées pour ce projet.")
            else:
                # Vérifier si l'extension existe déjà parmi les extensions utilisées pour ce département
                existing_used_extension = UsedExtension.objects.filter(name=extension_non_utilisee.name, department=department).exists()
                
                if existing_used_extension:
                    messages.error(request, "Cette extension existe déjà parmi les extensions utilisées pour ce département.")
                else:
                    extension_non_utilisee.save()
                    messages.success(request, "L'extension non utilisée a été ajoutée avec succès.")
                    return redirect('extensions_non_utilisees', department_id=department_id)
    
    else:
        form = AjouterExtensionNonUtiliseeForm()
    
    return render(request, 'departement/ajouter_extension_non_utilisee.html', {'form': form, 'department': department})


       
def ajouter_extension_utilisee(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    
    if request.method == 'POST':
        form = AjouterExtensionUtiliseeForm(request.POST)
        if form.is_valid():
            extension_utilisee = form.save(commit=False)
            extension_utilisee.department = department
            
            # Vérifier si l'extension existe déjà parmi les extensions utilisées pour ce département
            existing_extension = UsedExtension.objects.filter(name=extension_utilisee.name, department=department).exists()
            
            if existing_extension:
                messages.error(request, "Cette extension existe déjà dans les extensions utilisées pour ce département.")
            else:
                # Vérifier si l'extension existe déjà parmi les extensions non utilisées pour ce département
                existing_unused_extension = UnusedExtension.objects.filter(name=extension_utilisee.name, department=department).exists()
                
                if existing_unused_extension:
                    messages.error(request, "Cette extension existe déjà parmi les extensions non utilisées pour ce département.")
                else:
                    # Vérifier si le hostname existe déjà pour ce département
                    existing_hostname = UsedExtension.objects.filter(hostname=extension_utilisee.hostname, department=department).exists()
                    
                    if existing_hostname:
                        messages.error(request, "Ce hostname est déjà utilisé pour une autre extension dans ce département.")
                    else:
                        try:
                            extension_utilisee.save()
                            messages.success(request, "L'extension utilisée a été ajoutée avec succès.")
                            return redirect('extensions_utilisees', department_id=department_id)
                        except IntegrityError:
                            messages.error(request, "Une erreur d'intégrité est survenue lors de l'enregistrement de l'extension.")
    
    else:
        form = AjouterExtensionUtiliseeForm()
    
    return render(request, 'departement/ajouter_extension_utilisee.html', {'form': form, 'department': department})



def modifier_extension_non_utilisee(request, department_id, extension_id):
    department = get_object_or_404(Department, pk=department_id)
    extension_non_utilisee = get_object_or_404(UnusedExtension, pk=extension_id)
    
    if request.method == 'POST':
        form = ModifierExtensionNonUtiliseeForm(request.POST, instance=extension_non_utilisee)
        if form.is_valid():
            extension_modifiee = form.save(commit=False)
            
            # Vérifier si une extension avec le nouveau nom existe déjà pour ce département
            existing_used_extension = UsedExtension.objects.filter(name=extension_modifiee.name, department=department).exclude(pk=extension_id).exists()
            existing_unused_extension = UnusedExtension.objects.filter(name=extension_modifiee.name, department=department).exclude(pk=extension_id).exists()

            if existing_used_extension:
                messages.error(request, "Une extension avec ce nom existe déjà dans les extensions utilisées pour ce projet.")
            elif existing_unused_extension:
                messages.error(request, "Une extension non utilisée avec ce nom existe déjà dans ce projet.")
            else:
                extension_modifiee.save()
                messages.success(request, "L'extension non utilisée a été modifiée.")
                return redirect('extensions_non_utilisees', department_id=department_id)
    else:
        form = ModifierExtensionNonUtiliseeForm(instance=extension_non_utilisee)
    
    return render(request, 'departement/modifier_extension_non_utilisee.html', {'form': form, 'department': department})



def modifier_extension_utilisee(request, department_id, extension_id):
    department = get_object_or_404(Department, pk=department_id)
    extension_utilisee = get_object_or_404(UsedExtension, pk=extension_id)
    
    if request.method == 'POST':
        form = ModifierExtensionUtiliseeForm(request.POST, instance=extension_utilisee)
        if form.is_valid():
            extension_modifiee = form.save(commit=False)
            
            # Vérifier si un autre extension utilisee avec le même hostname existe déjà pour ce département
            existing_hostname = UsedExtension.objects.filter(
                hostname=extension_modifiee.hostname,
                department=department
            ).exclude(pk=extension_id).exists()
            
            if existing_hostname:
                messages.error(request, "Ce hostname est déjà utilisé pour une autre extension dans ce département.")
            else:
                extension_modifiee.save()
                messages.success(request, "L'extension utilisée a été modifiée.")
                return redirect('extensions_utilisees', department_id=department_id)
    else:
        form = ModifierExtensionUtiliseeForm(instance=extension_utilisee)
    
    return render(request, 'departement/modifier_extension_utilisee.html', {'form': form, 'department': department})



def supprimer_extensions_non_utilisees(request, department_id):
    if request.method == 'POST':
        extensions_ids = request.POST.getlist('extensions')
        deleted_count, _ = UnusedExtension.objects.filter(department_id=department_id, id__in=extensions_ids).delete()
        messages.success(request, f'{deleted_count} extension(s) non utilisée(s) supprimée(s).')
    return redirect('extensions_non_utilisees', department_id=department_id)

def supprimer_extension_non_utilisee(request, department_id, extension_id):
    # Récupérer le département
    department = get_object_or_404(Department, pk=department_id)
    
    # Récupérer l'extension non utilisée
    extension_non_utilisee = get_object_or_404(UnusedExtension, pk=extension_id)
    
    # Vérifier si la méthode de la requête est POST
    if request.method == 'POST':
        # Supprimer l'extension non utilisée
        extension_non_utilisee.delete()
        # Rediriger vers la page des extensions non utilisées pour ce département
        return redirect('extensions_non_utilisees', department_id=department_id)
    else:
        # Si la méthode de la requête n'est pas POST, rediriger également
        return redirect('extensions_non_utilisees', department_id=department_id)

def supprimer_extensions_utilisees(request, department_id):
    if request.method == 'POST':
        extensions_ids = request.POST.getlist('extensions')
        deleted_count, _ = UsedExtension.objects.filter(department_id=department_id, id__in=extensions_ids).delete()
        messages.success(request, f'{deleted_count} extension(s) utilisée(s) supprimée(s) avec succès.')
    return redirect('extensions_utilisees', department_id=department_id)

def supprimer_extension_utilisee(request, department_id, extension_id):
    # Récupérer le département
    department = get_object_or_404(Department, pk=department_id)
    
    # Récupérer l'extension utilisée en s'assurant qu'elle appartient au bon département
    extension_utilisee = get_object_or_404(UsedExtension, pk=extension_id, department_id=department_id)
    
    # Vérifier si la méthode de la requête est POST
    if request.method == 'POST':
        # Supprimer l'extension utilisée
        extension_utilisee.delete()
        messages.success(request, "L'extension utilisée a été supprimée avec succès.")
        # Rediriger vers la page des extensions utilisées pour ce département
        return redirect('extensions_utilisees', department_id=department_id)
    else:
        # Rendre une page de confirmation
        return render(request, 'departement/supprimer_extension_utilisee.html', {'extension': extension_utilisee, 'department': department})

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('extend')  # Rediriger vers la page souhaitée après connexion
            else:
                messages.error(request, "Identifiant ou mot de passe incorrect.")
        else:
            messages.error(request, "Erreur dans le formulaire.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accueil/index.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')


    

def export_used_extensions_by_department_excel(request, department_id):
    department = get_object_or_404(Department, pk=department_id)

    try:
        used_extensions = UsedExtension.objects.filter(department=department)

        # Créer un nouveau classeur Excel
        wb = Workbook()
        ws = wb.active
        ws.title = "Extensions Utilisées"

        # Ajouter les en-têtes avec les nouveaux champs
        ws.append(['Nom de l\'extension', 'Hostname', 'Floor', 'Position'])

        # Ajouter les extensions utilisées avec les nouveaux champs
        for extension in used_extensions:
            ws.append([extension.name, extension.hostname, extension.floor, extension.position])

        # Créer une réponse HTTP avec le contenu Excel en tant que fichier téléchargeable
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="extensions_utilisees_{department.name}.xlsx"'

        # Enregistrer le classeur Excel dans la réponse HTTP
        wb.save(response)

        messages.success(request, "L'exportation des extensions utilisées a été réalisée avec succès.")
        return response

    except Exception as e:
        messages.error(request, f"L'exportation des extensions utilisées a échoué : {str(e)}")
        return HttpResponseRedirect(reverse('extensions_utilisees', args=[department_id]))
    
def export_unused_extensions_by_department_excel(request, department_id):
    department = get_object_or_404(Department, pk=department_id)

    try:
        unused_extensions = UnusedExtension.objects.filter(department=department)

        # Créer un nouveau classeur Excel
        wb = Workbook()
        ws = wb.active
        ws.title = "Extensions Non Utilisées"

        # Ajouter les en-têtes
        ws.append(['Nom de l\'extension'])

        # Ajouter les extensions non utilisées
        for extension in unused_extensions:
            ws.append([extension.name])

        # Créer une réponse HTTP avec le contenu Excel en tant que fichier téléchargeable
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="extensions_non_utilisees_{department.name}.xlsx"'

        # Enregistrer le classeur Excel dans la réponse HTTP
        wb.save(response)

        messages.success(request, "L'exportation des extensions non utilisées a été réalisée avec succès.")
        return response

    except Exception as e:
        messages.error(request, f"L'exportation des extensions non utilisées a échoué : {str(e)}")
        return HttpResponseRedirect(reverse('extensions_non_utilisees', args=[department_id]))

@transaction.atomic
def import_used_extensions(request, department_id):
    department = get_object_or_404(Department, pk=department_id)

    if request.method == 'POST':
        form = ExtensionImportForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES.get('excel_file')
            if not excel_file:
                messages.error(request, 'Aucun fichier téléchargé.')
                return render(request, 'departement/import_used_extensions.html', {'form': form, 'department': department})

            try:
                df = pd.read_excel(excel_file)

                for index, row in df.iterrows():
                    extension_name = row.get('Nom_de_l_extension')
                    if not extension_name:
                        continue

                    hostname = row.get('Hostname')
                    floor = row.get('Floor')
                    position = row.get('Position')

                    existing_extension = UsedExtension.objects.filter(name=extension_name, department=department).first()
                    if existing_extension:
                        # L'extension existe déjà, mettre à jour les champs si nécessaire
                        existing_extension.hostname = hostname
                        existing_extension.floor = floor
                        existing_extension.position = position
                        existing_extension.save()
                    else:
                        # Créer une nouvelle extension utilisée avec les champs
                        UsedExtension.objects.create(
                            name=extension_name,
                            department=department,
                            hostname=hostname,
                            floor=floor,
                            position=position
                        )

                messages.success(request, 'Les extensions utilisées ont été importées avec succès.')
                return redirect('extensions_utilisees', department_id=department_id)

            except pd.errors.EmptyDataError:
                messages.error(request, 'Fichier vide ou format invalide.')
            except IntegrityError:
                messages.error(request, 'Une erreur d\'intégrité est survenue.')
            except Exception as e:
                messages.error(request, f'Une erreur est survenue : {str(e)}')

    else:
        form = ExtensionImportForm()

    return render(request, 'departement/import_used_extensions.html', {'form': form, 'department': department})


def import_unused_extensions(request, department_id):
    department = get_object_or_404(Department, pk=department_id)

    if request.method == 'POST':
        form = ExtensionImportForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES.get('excel_file')
            if not excel_file:
                messages.error(request, 'Aucun fichier téléchargé.')
                return render(request, 'departement/import_unused_extensions.html', {'form': form, 'department': department})

            try:
                df = pd.read_excel(excel_file)
                for index, row in df.iterrows():
                    extension_name = row.get('Nom_de_l_extension')
                    if not extension_name:
                        continue

                    # Vérifiez si l'extension existe déjà parmi les extensions utilisées
                    if UsedExtension.objects.filter(name=extension_name, department=department).exists():
                        messages.error(request, f"L'extension {extension_name} existe déjà parmi les extensions utilisées.")
                        continue

                    try:
                        UnusedExtension.objects.create(name=extension_name, department=department)
                    except IntegrityError:
                        # Si le nom de l'extension existe déjà, récupérer l'objet existant
                        existing_extension = UnusedExtension.objects.get(name=extension_name, department=department)
                        # Optionnel: Vous pouvez mettre à jour d'autres champs si nécessaire
                        existing_extension.save()
                messages.success(request, 'Les extensions non utilisées ont été importées avec succès.')
                return redirect('extensions_non_utilisees', department_id=department_id)
            except pd.errors.EmptyDataError:
                messages.error(request, 'Le fichier est vide ou le format est invalide.')
            except Exception as e:
                messages.error(request, f'Une erreur est survenue: {e}')
        else:
            messages.error(request, 'Le formulaire est invalide.')
    else:
        form = ExtensionImportForm()

    return render(request, 'departement/import_unused_extensions.html', {'form': form, 'department': department})


def gerer_extensions_utilisees(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    extension_ids = request.POST.getlist('extensions')
    action = request.POST.get('action')

    if not extension_ids:
        messages.error(request, "Veuillez sélectionner au moins une extension.")
        return redirect('extensions_utilisees', department_id=department_id)

    if action == 'supprimer':
        UsedExtension.objects.filter(department_id=department_id, id__in=extension_ids).delete()
        messages.success(request, "Extensions sélectionnées supprimées.")
    elif action == 'deplacer':
        for extension_id in extension_ids:
            used_extension = get_object_or_404(UsedExtension, pk=extension_id, department=department)
            
            # Vérifier si l'extension existe déjà dans les extensions non utilisées
            existing_unused_extension = UnusedExtension.objects.filter(name=used_extension.name, department=department).first()
            if existing_unused_extension:
                existing_unused_extension.delete()  # Supprimer l'extension existante

            # Créer une nouvelle extension non utilisée
            UnusedExtension.objects.create(name=used_extension.name, department=department)
            
            used_extension.delete()
        messages.success(request, "Extensions déplacées vers les extensions non utilisées.")

    return redirect('extensions_utilisees', department_id=department_id)


def gerer_extensions_non_utilisees(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    extension_ids = request.POST.getlist('extensions')
    action = request.POST.get('action')

    if not extension_ids:
        messages.error(request, "Veuillez sélectionner au moins une extension.")
        return redirect('extensions_non_utilisees', department_id=department_id)

    if action == 'supprimer':
        UnusedExtension.objects.filter(department_id=department_id, id__in=extension_ids).delete()
        messages.success(request, "extension(s) supprimée(s).")
    elif action == 'deplacer':
        for extension_id in extension_ids:
            unused_extension = get_object_or_404(UnusedExtension, pk=extension_id, department=department)
            
            # Vérifier si l'extension existe déjà dans les extensions utilisées
            existing_used_extension = UsedExtension.objects.filter(name=unused_extension.name, department=department).first()
            if existing_used_extension:
                existing_used_extension.delete()  # Supprimer l'extension existante

            # Créer une nouvelle extension utilisée
            UsedExtension.objects.create(name=unused_extension.name, department=department)
            
            unused_extension.delete()
        messages.success(request, "extension(s) déplacée(s) vers les extensions utilisées.")

    return redirect('extensions_non_utilisees', department_id=department_id)

def handel404(request, exception):
    return render(request, 'erreur/404.html')













