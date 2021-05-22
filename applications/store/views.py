from django.shortcuts import render, get_object_or_404
# Local Models
from .models import Product
# External Models
from applications.category.models import Category

# View: Search products by the given category
def store(request, category_slug=None):
    # Default values
    category = None
    products = None

    # If the user want to search the products by a category, then
    if category_slug != None:
        # Getting the category where the slug field from Category's model is equals to 'category_slug'
        category = get_object_or_404(Category, slug=category_slug)
        # Retrieving all the product according to the given category
        products = Product.objects.filter(category=category, is_available=True)
        # Counting the number of products that we have
        products_count = products.count()
    else:   
        # Retrieving only the products that are available
        products = Product.objects.all().filter(is_available=True)
        # Counting the number of products that we have
        products_count = products.count()

    # Passing the context to the render method, will make our products available inside the template
    context = {
        'products': products,
        'products_count': products_count,
    }

    # The store directory is created inside our template's directory
    return render(request,'store/store.html', context)
 
# View: Product Detail
def product_detail(request, category_slug, product_slug):
    # If the product doesn't exist
    try:
        # Retrieving a product by the given category and the given slug of the product
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)

    except Exception as e:
        raise e

    context = {
        'single_product' : single_product
    }

    return render(request, 'store/product_detail.html', context)
