# admin.py

from django.contrib import admin
from .models import Department, UsedExtension, UnusedExtension
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html


admin.site.site_header = "Gestionnaire IT Administration"
admin.site.site_title = "IT Gestionnaire"
admin.site.index_title = "Bienvenue sur l'interface d'administration"

class UsedExtensionInline(admin.TabularInline):
    model = UsedExtension

class UnusedExtensionInline(admin.TabularInline):
    model = UnusedExtension

class UsedExtensionAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'hostname', 'floor', 'position')  # Ajouter les nouveaux champs ici
    search_fields = ['name', 'department__name', 'hostname', 'floor', 'position']  # Champs de recherche étendus

class UnusedExtensionAdmin(admin.ModelAdmin):
    list_display = ('name', 'department')
    search_fields = ['name', 'department__name']

class DepartmentAdmin(admin.ModelAdmin):
    inlines = [UsedExtensionInline, UnusedExtensionInline]
    search_fields = ['name']

admin.site.register(Department, DepartmentAdmin)
admin.site.register(UsedExtension, UsedExtensionAdmin)
admin.site.register(UnusedExtension, UnusedExtensionAdmin)
