from django.urls import path
from . import views  # Importa las vistas de la app IdolPass
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('concerts/', views.concerts, name='concerts'),
    path('concert/<int:concert_id>/', views.concert_detail, name='concert_detail'),  # Cambié event_id por concert_id
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('concert/<int:concert_id>/', views.concert_detail, name='concert_detail'),
    path('cart/', views.shopping_cart, name='shopping_cart'),
    path('cart/remove/<int:ticket_id>/', views.remove_from_cart, name='remove_from_cart'),  # Ruta para eliminar tickets del carrito
    path('cart/add/<int:ticket_id>/', views.add_to_cart, name='add_to_cart'),  # Ruta para agregar tickets al carrito
    path('checkout/', views.checkout, name='checkout'),
    path('dashboard/', views.dashboard, name='dashboard'), # Ruta al Dashboard
    
    # Rutas para la edición y eliminación de conciertos
    path('concert/edit/<int:concert_id>/', views.edit_concert, name='concert_edit'),
    path('concert/delete/<int:concert_id>/', views.delete_concert, name='concert_delete'),
    path('concert/create/', views.create_concert, name='concert_create'),
    # Rutas para la edición y eliminación de usuarios
    path('user/edit/<int:user_id>/', views.edit_user, name='user_edit'),
    path('user/delete/<int:user_id>/', views.delete_user, name='user_delete'),
    path('user/create/', views.create_user, name='user_create'),
    # Rutas para la edición y eliminación de tickets
    path('ticket/edit/<int:ticket_id>/', views.edit_ticket, name='ticket_edit'),
    path('ticket/delete/<int:ticket_id>/', views.delete_ticket, name='ticket_delete'),
    path('ticket/create/', views.create_ticket, name='ticket_create'),

]
