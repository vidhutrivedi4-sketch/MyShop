from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('product/<int:id>/', views.product_detail, name='product_detail'),

    path('add/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('remove/<int:id>/', views.remove_from_cart, name='remove_from_cart'),

    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.success, name='success'),

    path('search/', views.search, name='search'),

    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('remove-all/<int:id>/', views.remove_all_from_cart, name='remove_all_from_cart'),

path('my-orders/', views.my_orders, name='my_orders'),
]