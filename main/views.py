from main.models import Artista, Etiqueta, UsuarioEtiquetaArtista, UsuarioArtista
from main.populateDB import populate
from main.forms import  UsuarioBusquedaForm, ArtistaBusquedaForm
from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponseRedirect
from django.conf import settings
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

    if request.method == 'POST':
        formulario = UsuarioBusquedaForm(request.POST)

        if formulario.is_valid():
            idusuario = formulario.cleaned_data['idUsuario']
            art_temp = UsuarioArtista.objects.filter(idUsuario=idusuario)
            artist = art_temp[1]
            artista = get_object_or_404(Artista, idArtista=artist.idArtista)
            tiempo = art_temp[2].tiempoEscucha

    return render(request, '5_artistas.html',
                  {'formulario': formulario, 'idusuario': idusuario, 'idartista': artista.idArtista, 'nombre_artista': artista.name, 
                   'tiempo': tiempo, 'STATIC_URL': settings.STATIC_URL})

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
