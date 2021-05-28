from django.contrib import admin
from .models import Product, Variation
# Register your models here

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'last_modified', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}

class VariationAdmin(admin.ModelAdmin):
    list_display  = ('product', 'variation_category', 'variation_value', 'is_active')
    # We can disable the product variation directly on the admin site, like so:
    list_editable = ('is_active', )
    # This filter will be displayed on the right-side of our admin site
    list_filter   = ('product', 'variation_category', 'variation_value')

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)

