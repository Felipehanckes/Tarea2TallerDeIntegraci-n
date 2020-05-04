from django.db import models

# Create your models here.

class Ingredient(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.TextField()

    def __str__(self):
        return "%s" % (self.nombre)

class Burguer(models.Model):
    nombre = models.CharField(max_length=30)
    precio = models.IntegerField()
    descripcion = models.TextField()
    imagen = models.TextField(blank=True)
    ingredientes = models.ManyToManyField(Ingredient, blank=True)

    def __str__(self):
        return "%s" % (self.nombre)