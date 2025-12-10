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
    fileobj = open(path + "\\artists.dat", "r", encoding='latin-1')
    for line in fileobj.readlines():
        rip = str(line.strip()).split("\t")
        if len(rip) != 4:
            a = Artista(idArtista=rip[0], nombre=rip[1], url=rip[2], pictureUrl="https://www.none.com") 
        else:
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
    fileobj = open(path + "\\tags.dat", "r", encoding='latin-1')
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
    fileobj=open(path + "\\user_artists.dat", "r", encoding='latin-1')
    fileobj.readline()
    for line in fileobj.readlines():
        rip = str(line.strip()).split("\t")
        lista.append(UsuarioArtista(idUsuario=rip[0], idArtista=a[rip[1]], tiempoEscucha=rip[2]))
    fileobj.close()
    UsuarioArtista.objects.bulk_create(lista)

def populateUserTagArtist(a, t):
    UsuarioEtiquetaArtista.objects.all().delete()

    lista=[]
    fileobj=open(path + "\\user_taggedartists.dat", "r", encoding='latin-1')
    fileobj.readline()
    for line in fileobj.readlines():
        rip = str(line.strip()).split("\t")
        date = datetime(int(rip[5]), int(rip[4]), int(rip[3]))
        #Hay un fallo porque no existe el artista 14103
        if rip[1] in a:
            lista.append(UsuarioEtiquetaArtista(idUsuario=rip[0], idArtista=a[rip[1]], idTagValue=t[rip[2]], fecha=date))
    fileobj.close()
    UsuarioEtiquetaArtista.objects.bulk_create(lista)
