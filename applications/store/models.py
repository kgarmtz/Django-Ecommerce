from django.db import models
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone


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
