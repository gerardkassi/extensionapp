from django.urls import path
from . import views




urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('charts/', views.charts, name='charts'),  # Correspond à la vue charts
    
    # Vue d'exportation
    path('departement/<int:department_id>/export-extensions-utilisees/', views.export_used_extensions_by_department_excel, name='export_used_extensions'),
    path('departement/<int:department_id>/export-extensions-non-utilisees/', views.export_unused_extensions_by_department_excel, name='export_unused_extensions'),

    # vue pour l'importation
    path('departement/<int:department_id>/import-extensions-utilisees/', views.import_used_extensions, name='import_used_extensions'),
    path('departement/<int:department_id>/import-extensions-non-utilisees/', views.import_unused_extensions, name='import_unused_extensions'),
    

    path('extend/', views.dashboard, name='extend'),  # Vue pour afficher tous les départements
    path('charts/', views.charts, name='charts'),  # Vue pour les graphiques

    
    # Vues pour les extensions utilisées et non utilisées par département
    path('departement/<int:department_id>/extensions-utilisees/', views.extension_utilisees, name='extensions_utilisees'),
    path('departement/<int:department_id>/extensions-non-utilisees/', views.extension_non_utilisees, name='extensions_non_utilisees'),

    # Vues pour ajouter une extension utilisée ou non utilisée pour un département spécifique
    path('departement/<int:department_id>/ajouter-extension-utilisee/', views.ajouter_extension_utilisee, name='ajouter_extension_utilisee'),
    path('departement/<int:department_id>/ajouter-extension-non-utilisee/', views.ajouter_extension_non_utilisee, name='ajouter_extension_non_utilisee'),

    # Vues pour modifier une extension utilisée ou non utilisée pour un département spécifique
    path('departement/<int:department_id>/modifier-extension-utilisee/<int:extension_id>/', views.modifier_extension_utilisee, name='modifier_extension_utilisee'),
    path('departement/<int:department_id>/modifier-extension-non-utilisee/<int:extension_id>/', views.modifier_extension_non_utilisee, name='modifier_extension_non_utilisee'),

    # Vues pour supprimer une extension utilisée ou non utilisée pour un département spécifique
    path('departement/<int:department_id>/supprimer-extension-utilisee/<int:extension_id>/', views.supprimer_extension_utilisee, name='supprimer_extension_utilisee'),
    path('departement/<int:department_id>/supprimer-extension-non-utilisee/<int:extension_id>/', views.supprimer_extension_non_utilisee, name='supprimer_extension_non_utilisee'),
    
    path('departments/<int:department_id>/supprimer_extensions_utilisees/', views.supprimer_extensions_utilisees, name='supprimer_extensions_utilisees'),
    path('supprimer-extensions-non-utilisees/<int:department_id>/', views.supprimer_extensions_non_utilisees, name='supprimer_extensions_non_utilisees'),
    #deplacer exentension 
    
    path('gerer-extensions-utilisees/<int:department_id>/', views.gerer_extensions_utilisees, name='gerer_extensions_utilisees'),
    path('gerer-extensions-non-utilisees/<int:department_id>/', views.gerer_extensions_non_utilisees, name='gerer_extensions_non_utilisees'),
    
]    



