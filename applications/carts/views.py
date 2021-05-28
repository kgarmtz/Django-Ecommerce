from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
# Local Models
from .models import Cart, CartItem
# External Models
from applications.store.models import Product, Variation

# Private Function: Retrieving the Session ID from a cookie on the browser
def _get_session_id(request):
    session_id = request.session.session_key
    if not session_id:
        session_id = request.session.create()
    # print(f'Session ID: {session_id}')
    return session_id


# View: Show the cart and all its items
def cart(request, cart_items=None):
    # This view gets executed everytime we invoke it using the 'redirect' function
    try:
        tax = 0
        grand_total = 0
        # Retrieving the current cart associated with the current session_id
        cart = Cart.objects.get(cart_id=_get_session_id(request))
        # Filtering out all the products according to the current cart
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        # Computing the total price
        total_price    = 0
        total_products = 0
        for cart_item in cart_items:
            total_price    += (cart_item.product.price * cart_item.quantity)
            total_products += cart_item.quantity
        # Tax of 2% applied in the final price
        tax = (2*total_price)/100
        # Calculating the grand total
        grand_total = total_price + tax

    except ObjectDoesNotExist:
        # Just ignore the cart and display an empty cart
        pass 
    
    # Defining our context dictionary 
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_products': total_products,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request, 'store/cart.html', context)

# View: Add to cart functionality
def add_to_cart(request, product_id):
    # Getting the product by the given product_id by the URL
    product = Product.objects.get(id=product_id)
    product_variations = []
    
    # Retrieving all the paramaters inside the browser URL sent by the user
    if request.method == 'POST':
        # print(f'add_to_cart | POST Request: {request.POST}')
        for variation_key in request.POST:
            variation_value = request.POST[variation_key]
            # Retrieving the variation object for one specific product, that matches with the data sent via POST method 
            try:
                # iexact is case-insensitive exact match  
                variation = Variation.objects.get(
                    product = product,
                    variation_category__iexact=variation_key, 
                    variation_value__iexact=variation_value)
                # Creating a variation's list that holds each product variation added to the current cart
                product_variations.append(variation)
            except:
                pass

    # If there's already a cart saved (Session ID was created)
    try: 
        # The cart_id will be equals to the Session ID stored on the browser
        cart = Cart.objects.get(cart_id=_get_session_id(request))
    
    # If the Cart doesn't exist, meaning there's no session ID created 
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _get_session_id(request)
        )
        # Saving the cart in the database
        cart.save()

    # Checking if the product sent in the URL is already in the Cart or Not
    is_cart_item_in_cart = CartItem.objects.filter(product=product, cart=cart).exists() 

    # Adding the products to the cart
    if is_cart_item_in_cart:
        # Getting all the CartItems from the Cart that correspond to the product sent in the URL  
        cart_items = CartItem.objects.filter(product=product, cart=cart)
        # Obtaining all the variations and the indices that all the cart_items found have
        existing_variations = []
        existing_indices    = []
        # We have to check if the variation of the product is already added in the Cart or not
        for cart_item in cart_items:
            existing_variations.append(list(cart_item.variations.all()))
            existing_indices.append(cart_item.id)
        
        print(f"Current variation: {product_variations}")
        print(f"Existing variations: {existing_variations}")
        # If the current variations 'product_variations' is in the existing_variations
        if product_variations in existing_variations:
            # Then, we have to retrieve the index of the CartItem that holds 'product_variations'
            index = existing_variations.index(product_variations)
            cart_item_id = existing_indices[index] 
            # Finally we have to retrive that CartItem from the Cart and increase its quantity
            cart_item = CartItem.objects.get(product=product,id=cart_item_id)
            cart_item.quantity += 1
            cart_item.save()
        
        else:
            # We have to create a new instance of CartItem for this product with its new variation
            cart_item = CartItem.objects.create(
                product = product,
                cart = cart,
                quantity = 1,
            )
            # We have to check if the product_variations is empty or not
            if product_variations:
                # Adding the variations for the product selected by the user
                cart_item.variations.add(*product_variations)
            # Saving the CartItem in the database
            cart_item.save()

    # If there's the first time that we add the product in the current cart
    else:
        # Creating and adding the item in our cart
        cart_item = CartItem.objects.create(
            product = product,
            cart = cart,
            quantity = 1,
        )

        if product_variations:
            # Many to Many filed uses the 'add' method to add elements to it
            cart_item.variations.add(*product_variations)
        # Saving the CartItem in the database 
        cart_item.save()

    return redirect('cart_app:cart')

# View: Decrease the aquantity for a product form cart functionality
def decrease_cart(request, product_id, cart_item_id):
    # Getting the current cart
    cart = Cart.objects.get(cart_id=_get_session_id(request))
    # Getting the product by the product_id
    product = get_object_or_404(Product, id=product_id)
    
    try:
        # Getting the product from the cart
        cart_item = CartItem.objects.get(id=cart_item_id, product=product, cart=cart)
        # If there's enough quantity to substract
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        # Otherwise, remove the product from the cart
        else:
            cart_item.delete()
    except:
        pass

    return redirect('cart_app:cart')
    
# View: Remove the whole item from cart when selectin the "Remove" button
def remove_cart(request, product_id, cart_item_id):
    # Getting the current cart
    cart = Cart.objects.get(cart_id=_get_session_id(request))
    # Getting the product by the product_id
    product = get_object_or_404(Product, id=product_id)
    try:
        # Getting the product from the cart
        cart_item = CartItem.objects.get(id=cart_item_id, product=product, cart=cart)
        # Removing the selected item from the cart
        cart_item.delete()
    except:
        pass
    
    return redirect('cart_app:cart')

