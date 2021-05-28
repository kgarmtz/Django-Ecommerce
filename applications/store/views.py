from django.shortcuts import render, get_object_or_404
# Logic operation OR in queries
from django.db.models import Q
# Paginator Functionality
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# Local Models
from .models import Product
# External Models
from applications.category.models import Category
from applications.carts.models import CartItem
# External Functions
from applications.carts.views import _get_session_id

# View: Filter products out by the given category
def store(request, category_slug=None):
    # Default values
    category = None
    products = None

    # If the user want to search the products by a category, then
    if category_slug != None:
        # Getting the category where the slug field from Category's model is equals to 'category_slug'
        category = get_object_or_404(Category, slug=category_slug)
        # Retrieving all the product according to the given category
        products = Product.objects.filter(category=category, is_available=True).order_by('id')

    else:   
        # Retrieving only the products that are available
        products = Product.objects.filter(is_available=True).order_by('id')
        # If we want to use a pagination, we have to order the QuerySet result

    # The Paginator class returns an "page_obj", we'll show 6 products per page
    paginator = Paginator(products, 6)
    # The URL has the form: url/?page=num_page, so we're retrieving the number of 'page'
    page = request.GET.get('page')
    # Getting all the products contained in the number of page given by the URL
    paged_products = paginator.get_page(page)
    # Counting the number of products that we have
    products_count = products.count()

    # Passing the context to the render method, will make our products available inside the template
    context = {
        'products': paged_products,
        'products_count': products_count,
    }

    # The store directory is created inside our template's directory
    return render(request,'store/store.html', context)
 
# View: Product Detail
def product_detail(request, category_slug, product_slug):
    try:
        # Retrieving a product by the given category and the given slug of the product
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        # Verifying if the product is already in one cart
        is_in_cart = CartItem.objects.filter(product=single_product, cart__cart_id=_get_session_id(request)).exists()
        # If the QuerySet contains any result, then the function 'exists' returns True, otherwise False

    # If the product doesn't exist
    except Exception as e:
        raise e

    context = {
        'single_product' : single_product,
        'is_in_cart': is_in_cart,
    }

    return render(request, 'store/product_detail.html', context)

# View: Searching products by the given keyword in the URL
def search_product(request):
    print(f'Search product | GET request: {request.GET}' )
    products = None
    products_count = 0
    # We have to recieve the <form> data that comes in the URL
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        # If the keyword is not an empty str ''
        if keyword:
            # Getting all the products where their description or name match wich the keyword sent by the user
            products = Product.objects.filter( 
                Q(product_name__icontains=keyword) | Q(description__icontains=keyword) 
            ).order_by('-creation_date')
            # Counting the number of products that we have
            products_count = products.count()

    context = {
        'products': products,
        'products_count': products_count,
    }

    return render(request,'store/store.html', context)
