'''from django.urls import path
from . import views

urlpatterns = [
    #path('', views.index, name='index'),  # Route principale
    path('upload/', views.upload, name='upload'),
    path('stats/', views.stats, name='stats'),
    path('visualize/', views.visualize, name='visualize'),
]'''

'''from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload, name='upload'),
    path('stats/', views.stats, name='stats'),
    path('visualize/', views.visualize, name='visualize'),
]'''

from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),  # Ajoutez cette ligne si manquante
    #path('', views.index, name='index'),  # L'URL de la page d'accueil
    path('', views.upload, name='upload'),  # Assurez-vous que cette ligne est correcte
    path('stats/', views.stats, name='stats'),
    path('visualize/', views.visualize, name='visualize'),
    path('download-graph/', views.download_graph, name='download_graph'),
]
