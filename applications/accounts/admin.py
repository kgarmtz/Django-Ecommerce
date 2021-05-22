from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

# Adding this class allows us to edit and declare which fields will show in the admin site
class AccountAdmin(UserAdmin):
    # Each field declared in 'list_display' will be showned at the table of the Accounts model as a column 
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active') 
    # We can define fields that when we click on them we can register (in this case) a new Account 
    list_display_links = ('email', 'first_name', 'last_name')
    # Specifying the read-only fields in the admin site
    readonly_fields = ('last_login', 'date_joined')
    # Ordering the users in descending order 
    ordering = ('-date_joined',)
    # Creating a filter that will filter out the user by first_name and last_name
    list_filter = ('first_name', 'last_name')
    filter_horizontal = ()
    # We use fieldsets to make the 'password' read-only
    fieldsets = ()


# Register the model with their custom admin site
admin.site.register(Account, AccountAdmin)    

    