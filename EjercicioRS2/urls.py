from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index.html/', views.index),
    path('populate/', views.populateDatabase),
    path('ingresar/', views.ingresar),
    path('', views.index),
    path('cinco_artistas_mas_escuchado_de_usuario/', views.mostrar_artistas_usuario),
    path('diez_etiquetas_mas_frecuentes_de_usuarios_por_artista/', views.mostrar_etiquetas_artistas),
    path('recomendar_artistas_usuario_RSusuario/', views.recomendar_artistas_usuario_RSusuario),
    path('recomendar_artistas_usuario_RSitems/', views.recomendar_artistas_usuario_RSitems),
    path('loadRS/', views.loadRS),
]
