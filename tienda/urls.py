from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import agregar_producto, agregar_categoria, categorias

urlpatterns = [
    path('', views.categorias, name='categorias'),
    path('categorias/', categorias, name='categorias'),
    path('categoria/<int:categoria_id>/', views.productos_por_categoria, name='productos_por_categoria'),
    path('agregar_al_carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('ver_carrito/', views.ver_carrito, name='ver_carrito'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('accounts/profile/', views.profile, name='profile'),
    path('agregar_producto/', agregar_producto, name='agregar_producto'),
    path('agregar_categoria/', agregar_categoria, name='agregar_categoria'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
