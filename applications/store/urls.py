from django.urls import path
from . import views

# Naming the urlpatterns as a whole
app_name = 'store_app'

urlpatterns = [
    # We have two URLs that occupy the same view
    path('store/', views.store, name='store'),
    # We're sending to our view the 'category_slug' parameter which is sent in the URL 
    path('store/<slug:category_slug>/', views.store, name='products_by_category'),
    # URL for the product detail
    path('store/<slug:category_slug>/<slug:product_slug>', views.product_detail, name='product_detail'),

]