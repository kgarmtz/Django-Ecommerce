# Declaring the global variables that we want to display in the whole qpplication
from .models import Cart, CartItem
# Local Functions
from .views import _get_session_id, cart

# The context processor's functions are always get executed 
def product_counter(request):
    print(f'Request Path from Context Processor: {request.path}')
    cart_products = 0
    # If a SuperUser is in the site
    if 'admin' in request.path:
        return {}
    else:
        # If there's a Cart Shopping already saved
        try:
            # Retrieving the current cart associated with the current session_id
            cart = Cart.objects.get(cart_id=_get_session_id(request))
            # Retrieving all the product inside the current cart
            card_items = CartItem.objects.filter(cart=cart)
            # Computing the total quantity of products
            for card_item in card_items:
                cart_products += card_item.quantity
        # If there's no Cart Shopping yet
        except Cart.DoesNotExist:
            cart_products = 0
    
    return {
        'cart_products': cart_products
    }
                    

          