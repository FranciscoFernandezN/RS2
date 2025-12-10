from django.db import models

class Artista(models.Model):
    idArtista = models.TextField(primary_key=True)
    nombre = models.TextField(verbose_name='Nombre',max_length=100)
    url = models.URLField(verbose_name='URL')
    pictureUrl = models.URLField(verbose_name='Picture URL')

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ('nombre',)

class Etiqueta(models.Model):
    idTag = models.TextField(primary_key=True)
    tagValue = models.TextField(verbose_name='Tag Value')
    def __str__(self):
        return self.idTag

class UsuarioArtista(models.Model):
    idUsuario = models.TextField(verbose_name='Id del usuario')
    idArtista = models.ForeignKey(Artista, on_delete=models.CASCADE)
    tiempoEscucha = models.IntegerField()

    def __str__(self):
        return self.tiempoEscucha

class UsuarioEtiquetaArtista(models.Model):
    idUsuario = models.TextField(verbose_name='Id del usuario')
    idArtista = models.ForeignKey(Artista, on_delete=models.CASCADE)
    idTagValue = models.ForeignKey(Etiqueta, on_delete=models.CASCADE)
    fecha = models.DateField(verbose_name='Fecha de escucha')

    def __str__(self):
        return self.fecha