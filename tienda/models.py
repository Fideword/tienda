from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='productos/')
    def __str__(self):
        return self.nombre

class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    productos = models.ManyToManyField('Producto', through='ItemCarrito')

class ItemCarrito(models.Model):
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    carrito = models.ForeignKey('Carrito', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

