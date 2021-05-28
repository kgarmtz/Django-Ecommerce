from django.db import models

# External Models
from applications.accounts.models import Account
from applications.store.models import Product, Variation

# Create your models here.
class Cart(models.Model):
    # This cart_id will be stored in the Session Cookie as Session ID
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    # One Product can be relationated to many CardItems
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # One CartItem can have many Variations and one Variation can belong to many CartItems
    variations = models.ManyToManyField(Variation, blank=True)
    # One Cart can have to many CartItems, but one CartItem must belong only to one Cart
    cart    = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity
 
    # To print an instance model (object), we can use the '__unicode__' method
    def __str__(self):
        return 'Cart: ' + str(self.cart.cart_id) + ': '+ self.product.product_name


    