from django.shortcuts import render, get_object_or_404, redirect
from .models import Categoria, Producto, Carrito, ItemCarrito
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import ProductoForm, CategoriaForm

# Create your views here.
def categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'tienda/categorias.html', {'categorias': categorias})

def productos_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    productos = Producto.objects.filter(categoria=categoria)
    return render(request, 'tienda/productos.html', {'categoria': categoria, 'productos': productos})

@login_required
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            nuevo_producto = form.save(commit=False)
            nuevo_producto.save()
            return redirect('categorias')
    else:
        form = ProductoForm()

    return render(request, 'tienda/agregar_producto.html', {'form': form})

def agregar_al_carrito(request, producto_id):
    if request.method == 'POST':
        producto = get_object_or_404(Producto, pk=producto_id)
        if request.user.is_authenticated:
            carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
            item, creado = ItemCarrito.objects.get_or_create(producto=producto, carrito=carrito)
            if not creado:
                item.cantidad += 1
                item.save()
        return redirect('ver_carrito')
    return redirect('categorias')

def agregar_categoria_al_carrito(request, categoria_id):
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    if request.user.is_authenticated:
        carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
        productos_en_categoria = Producto.objects.filter(categoria=categoria)
        for producto in productos_en_categoria:
            item, creado = ItemCarrito.objects.get_or_create(producto=producto, carrito=carrito)
            if not creado:
                item.cantidad += 1
                item.save()
    return redirect('ver_carrito')

@login_required
def agregar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            nueva_categoria = form.save()
            return redirect('categorias')
    else:
        form = CategoriaForm()

    return render(request, 'tienda/agregar_categoria.html', {'form': form})

def ver_carrito(request):
    if request.user.is_authenticated:
        carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
        items = carrito.itemcarrito_set.all()
    else:
        items = []
    return render(request, 'tienda/carrito.html', {'items': items})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Inicia sesión después del registro
            return redirect('categorias')  # Redirige a la página principal
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    # Obtener el usuario actual
    user = request.user

    # Puedes acceder a la información del usuario, por ejemplo:
    username = user.username
    email = user.email
    first_name = user.first_name
    last_name = user.last_name

    return render(request, 'tienda/profile.html', {
        'user': user,
        'username': username,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
    })

    
