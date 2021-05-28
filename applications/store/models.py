from django.db import models
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
# Local Managers
from .managers import VariationManager


# Importing our Category model
from applications.category.models import Category

class TimeStamped(models.Model):
    # editable=False: The fields cannot be editable in the admin site
    creation_date = models.DateTimeField(editable=False)
    last_modified = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        print("Updating the date automatically")
        # If the instance of the model is not registered yet
        if not self.creation_date:
            self.creation_date = timezone.now()

        self.last_modified = timezone.now()
        return super(TimeStamped, self).save(*args, **kwargs)

    class Meta:
        abstract = True


# Register your models here.
class Product(TimeStamped):
    product_name    = models.CharField(max_length=200, unique=True)
    slug            = models.SlugField(max_length=200, unique=True)
    description     = models.TextField(max_length=500, blank=True)
    price           = models.IntegerField()
    images          = models.ImageField(upload_to='photos/products')
    stock           = models.IntegerField()
    is_available    = models.BooleanField(default=True)
    # What would happen to the Product once we delete a Category?
    # Whenever we delete a category all the products attached to that
    # Category will be deleted  
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)

    # self - An instance of the Model's Product
    def get_url(self):
        # reverse is the same as {% url 'absolute_path' %} that we use in our templates
        return reverse('store_app:product_detail', args=[self.category.slug, self.slug])

    # String representation of our model
    def __str__(self):
        return self.product_name



class Variation(models.Model):
    # variation_category choices 
    VARIATION_CHOICES = (
        ('color', 'color'),
        ('size', 'size'),
    )
    
    # One product can have many variations, if we doesn't provide the 'related_name' parameter
    # we can access instead by giving the default name of the manager, that's 'variation_set'  
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations')
    # We can select the variation that the product will have. It can be color or size
    variation_category = models.CharField(max_length=100, choices=VARIATION_CHOICES)
    # We can specify the corresponding value to the variation_category that was selected.
    #  Ex.  variation_category = color and then variation_value = red
    variation_value     = models.CharField(max_length=100)
    # This field is useful when we want to disable any of the product variations 
    is_active           = models.BooleanField(default=True)
    created_date        = models.DateTimeField(auto_now=True)
    # Linking the custom manager for this model
    objects = VariationManager()

    # String representation of our model
    def __str__(self):
        return self.variation_value
        # return self.product.product_name + ': ' + self.variation_value

