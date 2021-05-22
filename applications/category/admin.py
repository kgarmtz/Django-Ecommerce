from django.contrib import admin
from .models import Category

# Using a decorator to personalize our Category model in the admin site
class CategoryAdmin(admin.ModelAdmin):
    # The main use for this functionality is to automatically generate the value
    #  for SlugField fields from one or more other fields. 
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'slug')

# Register your models here.
admin.site.register(Category, CategoryAdmin)

