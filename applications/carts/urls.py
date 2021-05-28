from django.urls import path
from . import views 

# Naming the whole urlpatterns
app_name = 'cart_app'

urlpatterns = [
    # The base URL is declared in the main urls.py file as 'cart/'
    path('', views.cart, name='cart'),
    path('add_cart/<int:product_id>/', views.add_to_cart, name='add_cart'),
    path('decrease_cart/<int:product_id>/<int:cart_item_id>/', views.decrease_cart, name='decrease_cart'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/', views.remove_cart, name='remove_cart'),
]