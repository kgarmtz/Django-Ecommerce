from django.shortcuts import render
from applications.store.models import Product


# The render method returns and HTML document
def home(request):
     # Passing to the template only the products that are available
    products = Product.objects.all().filter(is_available=True)
    # Declaring the context dictionary that will be sended to the template
    context = {
        'products': products,
    }

    return render(request, 'home.html', context)