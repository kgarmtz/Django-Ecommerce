from django.http.response import HttpResponse
from django.shortcuts import render, redirect
# Import for adding Django messages to our view
from django.contrib import messages
from django.contrib.auth import authenticate
# We do this in order to avoid a TypeError between the functions that have the same name
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
# Login Decorator
from django.contrib.auth.decorators import login_required
# Django sites framework
from django.contrib.sites.shortcuts import get_current_site
# Imports for the Verification Email Process
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
# Local Models
from .models import Account
# External Models
from applications.carts.models import Cart, CartItem
# Local Forms
from .forms import RegistrationForm
# External View Functions
from applications.carts.views import _get_session_id
# Third Party Apps
import requests


# View: Register a new user in our system
def register(request):

    if request.method == 'POST':
        # Creating an instance of the form with the user-data
        form = RegistrationForm(request.POST)
        # Valitaing the form to access to the cleaned_data attribute
        if form.is_valid():
            # Once the form is valid, we can access to the cleaned_data dictionary
            first_name   = form.cleaned_data['first_name']
            last_name    = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email        = form.cleaned_data['email']
            password     = form.cleaned_data['password']
            # Assign a username based on the email
            username = email.split('@')[0]
            # Creating the user account
            user = Account.objects._create_user(
                first_name=first_name, 
                last_name=last_name, 
                email=email, 
                username=username, 
                password=password
            )
            # Adding the phone number to the user instance
            user.phone_number = phone_number
            user.save()
            """ USER ACTIVATION PROCESS
            Retrieving the current Site object (domain and name) based on the request
            That's necessary because the default domain is localhost, but when the site
            is on production side, it will change """
            current_site = get_current_site(request)
            email_subject = 'Please activate your account'
            email_body = render_to_string('accounts/email_verification.html', {
                'user': user,
                'domain': current_site,
                # We must enconding the user primary key because we're going to send 
                # it throuhg the URL for the activation process when the user start
                # the verification process (click on the link we sent to his email)
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # Creating a token (verification code) for this particular user, the
                # generated token is actually a one-use one and exclusive for this user.
                'token': default_token_generator.make_token(user) 
            })

            email_recipient = email
            # Sending an email to the user email
            send_email = EmailMessage( email_subject, email_body, to=[email_recipient])
            send_email.send()

            # If everything went well, we display a proper message to the user
            # messages.success(request, 'Registration successful.')
            return redirect(f'/account/login/?command=verification&email={email}')
        
    else:
        # Assigning the created form to the view and render it to the template
        form = RegistrationForm()
    
    # Passing the whole form to our template
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)

# View: Login authentication
def login(request):
    print(f'POST-LOGIN: {request.POST}')
    if request.method == 'POST':
        # Retrieving the email and the password sent in the URL by the POST request
        email    = request.POST['email']
        password = request.POST['password']
        # Verifying if the user email and password are valid
        user = authenticate(email=email, password=password)
        # If the user gets authenticated successfully in our system, then
        if user is not None:
            try:
                # Before the login process, we have to check if there're already CartItems added
                cart = Cart.objects.get(cart_id=_get_session_id(request))
                # Verifying if the current Cart has CartItems
                is_any_cart_item = CartItem.objects.filter(cart=cart).exists()

                if is_any_cart_item:
                    # Getting all the CartItems inside the current Cart
                    cart_items = CartItem.objects.filter(cart=cart)
                    # Product: Shirt, Variations: Blue and Large
                    cart_variations = []
                    cart_indices = []
                    # Getting all the CartItem variations form the current Cart
                    for cart_item in cart_items:
                        variations = cart_item.variations.all()
                        # Where the variation gets positioned in list, the index will be in the same position
                        cart_variations.append(list(variations))
                        cart_indices.append(cart_item.id)
                        
                    # Getting all the CartItem variations from all the user products that's about to login
                    user_items = CartItem.objects.filter(user=user)
                    # Obtaining all the variations and the indices that all the user_items found have
                    user_variations  = []
                    existing_indices = []
                    # Adding all the user_item variations inside their corresponding list
                    for user_item in user_items:
                        # Saving the variations of that particular CartItem
                        user_variations.append(list(user_item.variations.all()))
                        # Saving the index of that particular CartItem 
                        existing_indices.append(user_item.id)

                    # We have to compare the cart_variations (current Cart) with the user_variations (current User)
                    for cart_variation in cart_variations:
                        if cart_variation in user_variations:
                            # Getting the index of the "cart_variation" inside the list of user_variations
                            index = user_variations.index(cart_variation)
                            user_item_id = existing_indices[index]
                            # Finally we have to retrive that CartItem from the user Cart and increase its quantity
                            user_item = CartItem.objects.get(id=user_item_id) 
                            user_item.quantity += 1
                            user_item.save()
                        else:
                            print(f"CURRENT VARIATIONS LIST: {cart_variation}")
                            index = cart_variations.index(cart_variation)
                            cart_item_id = cart_indices[index]
                            cart_item = CartItem.objects.get(id=cart_item_id)
                            cart_item.user = user
                            cart_item.save()

            # The except gets executed if we don't have any CartItem inside the Cart
            except:
                pass
            
            auth_login(request, user)
            messages.success(request, 'You are now logged in')
            # If the user comes from the "/cart/checkout/" it means the
            # he already has products inside his Cart
            # HTTP_REFERER: It returns the page from what you came from 
            previous_url = request.META.get('HTTP_REFERER')
            print(f'PREVIOUS URL: {previous_url}')
            try:
                # From this url: http://127.0.0.1:8000/account/login/?next=/cart/checkout/
                # We store inside 'query': next=/cart/checkout/ 
                query = requests.utils.urlparse(previous_url).query
                key, url = query.split('=')
                params = {
                    key: url
                }
                
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('account_app:dashboard')

        else:
            messages.error(request, 'Invalid login credentials')
            return  redirect('account_app:login')

    return render(request, 'accounts/login.html')
    
""" We only can logout if we're already login in the system
Otherwise, we cannot access to this view, so to ensure that
this situation happens, we use a decorator..."""

@login_required(login_url= 'account_app:login')
def logout(request):
    auth_logout(request)
    messages.success(request, 'You are logged out')
    return redirect('account_app:login')

# View for activating a user account, it sets the is_active to True
def activate(request, uidb64, token):
    
    try:
        # Decoding the user primary key
        uid = urlsafe_base64_decode(uidb64).decode()
        # When we're using a custom Manager objects and if we want
        # to use the default Manager that Django creates instead...
        user = Account._default_manager.get(pk=uid)

    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    # If the user can be retrieved successfully and the token sent in the URL
    # corresponds to the token that we created exclusively for the user...
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account has been activated.')
        return redirect('account_app:login')
    else:
        messages.error(request, 'Invalid activation link.')
        return redirect('account_app:register')

# View: User dashboard that shows all the orders made by the user, also
# If any user wants to access to this view it has to be logged in first.
@login_required(login_url= 'account_app:login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

# RESET PASSWORD PROCESS

# View: If a user forgets their password 
def forgotPassword(request):
    if request.method == 'POST':
        # Retrieving the email from the POST request
        email = request.POST['email']
        # Checking if a user already exists with the given email
        if Account.objects.filter(email=email).exists():
            # Retrieving the user with the given email (unique type field)
            user = Account.objects.get(email__exact=email)
            # Sending the email to the user to reset their password
            current_site = get_current_site(request)
            email_subject = 'Reset your password'
            email_body = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user) 
            })

            email_recipient = email
            # Sending an email to the user email
            send_email = EmailMessage( email_subject, email_body, to=[email_recipient])
            send_email.send()
            messages.success(request, f'Password reset link has been sent to {email}')
            return redirect('account_app:login')

        else:
            # If an account can be found in the system
            messages.error(request, f'Account does not exist!')
            return redirect('account_app:forgot-password')

    else:
        return render(request, 'accounts/forgotPassword.html')

# View: Validating the user crendentials before the reseting password process
def resetPasswordValidate(request, uidb64, token):
    
    try:
        # Decoding the user primary key
        uid = urlsafe_base64_decode(uidb64).decode()
        # When we're using a custom Manager objects and if we want
        # to use the default Manager that Django creates instead...
        user = Account._default_manager.get(pk=uid)

    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    # We use check_token to ensure that the user request is secure 
    if user is not None and default_token_generator.check_token(user, token):
        # Saving the user primary key in the current session
        request.session['uid'] = uid
        print(f'resetPassword - Current Session: {uid}')
        messages.success(request, 'Please enter your new password')
        return redirect('account_app:reset-password')

    # if the user does not exits or the token is already expired
    else:
        messages.error(request, 'The reset password link has been expired.')
        return redirect('account_app:login')

# View: Reset Password Process
def resetPassword(request):

    if request.method == 'POST':
        password         = request.POST['password']
        confirm_password = request.POST['confirm_password']
        # If the password match
        if password == confirm_password:
            # Retrieving the user uid from the request.session that we stored previously
            uid = request.session['uid']
            print(f'resetPassword - Session Saved: {uid}')
            # Getting the user that corresponds with that 'uid'
            user = Account.objects.get(pk=uid)
            # The set_password function saves the user password safely in the database
            user.set_password(password)
            # Saving the changes
            user.save()
            messages.success(request, 'Password has been changed successfully')
            return redirect('account_app:login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('account_app:reset-password')
    else:
        return render(request, 'accounts/resetPassword.html')