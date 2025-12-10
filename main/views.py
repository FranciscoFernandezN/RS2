from matplotlib import artist

from main.models import Artista, Etiqueta, UsuarioEtiquetaArtista, UsuarioArtista
from main.populateDB import populate
from main.forms import  UsuarioBusquedaForm, ArtistaBusquedaForm
from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponseRedirect
from django.conf import settings
from django.db.models import Count
#from main.recommendations import  transformPrefs, calculateSimilarItems, getRecommendations, getRecommendedItems, topMatches
import shelve

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

#Funcion de acceso restringido que carga los datos en la BD
@login_required(login_url='/ingresar')
def populateDatabase(request):
    populate()
    logout(request)  # se hace logout para obligar a login cada vez que se vaya a poblar la BD
    return HttpResponseRedirect('/index.html')


def mostrar_artistas_usuario(request):
    formulario = UsuarioBusquedaForm()
    idusuario = None
    artistas = []

    if request.method == 'POST':
        formulario = UsuarioBusquedaForm(request.POST)

        if formulario.is_valid():
            idusuario = formulario.cleaned_data['idUsuario']
    
            top_tags_qs = (UsuarioArtista.objects
                           .filter(idUsuario=idusuario)
                           .order_by('-tiempoEscucha')[:5])
            

            # Construir lista de tuplas (Etiqueta, frecuencia) en el mismo orden
            for entry in top_tags_qs:
                artistas_obj = entry.idArtista
                
                artistas.append((artistas_obj, entry.tiempoEscucha))


    return render(request, '5_artistas.html',
                  {'formulario': formulario, 'items': artistas, 'idusuario': idusuario, 'STATIC_URL': settings.STATIC_URL})

def mostrar_etiquetas_artistas(request):
    formulario = ArtistaBusquedaForm()
    idartista = None
    etiquetas = []

    if request.method == 'POST':
        formulario = ArtistaBusquedaForm(request.POST)
    
        if formulario.is_valid():
            idartista = formulario.cleaned_data['idArtista']
            # Obtener todas las entradas de etiquetas para este artista,
            # agrupar por idTagValue y contar ocurrencias, ordenando por frecuencia.
            top_tags_qs = (UsuarioEtiquetaArtista.objects
                           .filter(idArtista=idartista)
                           .values('idTagValue')
                           .annotate(freq=Count('idTagValue'))
                           .order_by('-freq')[:10])

            # Construir lista de tuplas (Etiqueta, frecuencia) en el mismo orden
            for entry in top_tags_qs:
                tid = entry['idTagValue']
                etiqueta_obj = get_object_or_404(Etiqueta, pk=tid)
                
                etiquetas.append(etiqueta_obj)

    return render(request, '10_etiquetas_artistas.html',
                  {'formulario': formulario,
                   'idartista': idartista,
                   'tags': etiquetas,
                   'STATIC_URL': settings.STATIC_URL})

def index(request):
    return render(request, 'index.html',{'STATIC_URL':settings.STATIC_URL})

def ingresar(request):
    formulario = AuthenticationForm()
    if request.method=='POST':
        formulario = AuthenticationForm(request.POST)
        usuario=request.POST['username']
        clave=request.POST['password']
        acceso=authenticate(username=usuario,password=clave)
        if acceso is not None:
            if acceso.is_active:
                login(request, acceso)
                return (HttpResponseRedirect('/populate'))
            else:
                return render(request, 'mensaje_error.html',{'error':"USUARIO NO ACTIVO",'STATIC_URL':settings.STATIC_URL})
        else:
            return render(request, 'mensaje_error.html',{'error':"USUARIO O CONTRASEÑA INCORRECTOS",'STATIC_URL':settings.STATIC_URL})
                     
    return render(request, 'ingresar.html', {'formulario':formulario, 'STATIC_URL':settings.STATIC_URL})
