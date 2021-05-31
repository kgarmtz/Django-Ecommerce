from django.urls import path
# Local views
from . import views

# Naming the whole urlpatterns
app_name = 'account_app'
# The base URL is declared in the main urls.py file as 'account/'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # If a user try to access to accounts/ url it'll show an error message
    # To avoid that, we can stablish a default url for this
    path('', views.dashboard, name='dashboard'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgotPassword/', views.forgotPassword, name='forgot-password'),
    
    # Reset Password Process: Validate the user credentials.
    path('resetPasswordValidate/<uidb64>/<token>/', views.resetPasswordValidate, name='reset-password-validate'),
    # Reset Password Process: Reset the password
    path('resetPassword/', views.resetPassword, name='reset-password'),
]