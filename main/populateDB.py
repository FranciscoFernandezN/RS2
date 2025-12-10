from main.models import Artista, Etiqueta, UsuarioArtista, UsuarioEtiquetaArtista
from datetime import datetime

path = "data"

def populate():
    a = populateArtist()
    t = populateTag()
    populateUserArtist(a)
    populateUserTagArtist(a, t)

def populateArtist():
    Artista.objects.all().delete()

    lista = []
    dict = {}
    fileobj = open(path + "\\artists.dat", "r")
    fileobj.readline()
    for line in fileobj.readlines():
        rip = str(line.strip()).split("\t")
        if len(rip) != 4:
            continue
        a = Artista(idArtista=rip[0], nombre=rip[1], url=rip[2], pictureUrl=rip[3])
        lista.append(a)
        dict[rip[0]] = a
    fileobj.close()
    Artista.objects.bulk_create(lista)

    return(dict)

def populateTag():
    Etiqueta.objects.all().delete()

    lista = []
    dict = {}
    fileobj = open(path + "\\tags.dat", "r")
    fileobj.readline()
    for line in fileobj.readlines():
        rip = str(line.strip()).split("\t")
        if len(rip) != 2:
            continue
        e = Etiqueta(idTag=rip[0], tagValue=rip[1])
        lista.append(e)
        dict[rip[0]] = e
    fileobj.close()
    Etiqueta.objects.bulk_create(lista)

    return(dict)

def populateUserArtist(a):
    UsuarioArtista.objects.all().delete()

    lista=[]
    fileobj=open(path + "\\user_artists.dat", "r")
    fileobj.readline()
    for line in fileobj.readlines():
        rip = str(line.strip()).split("\t")
        lista.append(UsuarioArtista(idUsuario=rip[0], idArtista=a[rip[1]], tiempoEscucha=rip[2]))
    fileobj.close()
    UsuarioArtista.objects.bulk_create(lista)

def populateUserTagArtist(a, t):
    UsuarioEtiquetaArtista.objects.all().delete()

    lista=[]
    fileobj=open(path + "\\user_taggedartists.dat", "r")
    fileobj.readline()
    for line in fileobj.readlines():
        rip = str(line.strip()).split("\t")
        date = datetime.datetime(rip[5], rip[4], rip[3])
        lista.append(UsuarioEtiquetaArtista(idUsuario=rip[0], idArtista=rip[1], idTagValue=rip[2], fecha=date))
    fileobj.close()
    UsuarioEtiquetaArtista.objects.bulk_create(lista)
