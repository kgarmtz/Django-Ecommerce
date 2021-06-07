# Declaring the global variables that we want to display in the whole qpplication
from .models import Cart, CartItem
# Local Functions
from .views import _get_session_id

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
            print(f'CART-ID from Context Processor: {_get_session_id(request)}')
            # If the user is authenticated, then is logged in
            if request.user.is_authenticated:
                # Getting all the user CarItems
                cart_items = CartItem.objects.filter(user=request.user)
            else:
                # Retrieving the current cart associated with the current session_id    
                # We use 'filter' because when the user logged in the system the 
                # session_id changed, that's why we cannot use 'get' 
                cart = Cart.objects.filter(cart_id=_get_session_id(request))
                # Retrieving all the product inside the current cart
                cart_items = CartItem.objects.filter(cart=cart[:1])

            # Computing the total quantity of products
            for cart_item in cart_items:
                cart_products += cart_item.quantity

        # If there's no Cart Shopping yet
        except Cart.DoesNotExist:
            cart_products = 0
    
    return {
        'cart_products': cart_products
    }
                    

          