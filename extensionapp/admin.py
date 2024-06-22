from django.contrib import admin
from .models import Department, UsedExtension, UnusedExtension
from django.utils.translation import gettext_lazy as _

admin.site.site_header = _("Gestionnaire IT Administration")
admin.site.site_title = _("IT Gestionnaire")
admin.site.index_title = _("Bienvenue sur l'interface d'administration")

class UsedExtensionInline(admin.TabularInline):
    model = UsedExtension

class UnusedExtensionInline(admin.TabularInline):
    model = UnusedExtension

class UsedExtensionAdmin(admin.ModelAdmin):
    list_display = ('name', 'department')
    search_fields = ['name', 'department__name']

class UnusedExtensionAdmin(admin.ModelAdmin):
    list_display = ('name', 'department')
    search_fields = ['name', 'department__name']

class DepartmentAdmin(admin.ModelAdmin):
    inlines = [UsedExtensionInline, UnusedExtensionInline]
    search_fields = ['name']

   

admin.site.register(Department, DepartmentAdmin)
admin.site.register(UsedExtension, UsedExtensionAdmin)
admin.site.register(UnusedExtension, UnusedExtensionAdmin)
