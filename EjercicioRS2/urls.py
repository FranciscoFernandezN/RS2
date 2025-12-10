from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index.html/', views.index),
    path('populate/', views.populateDatabase),
    path('ingresar/', views.ingresar),
    path('', views.index),
    path('cinco_artistas_mas_escuchado_de_usuario/', views.mostrar_artistas_usuario)
]
