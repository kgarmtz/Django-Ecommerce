from django.db import models
from django.urls import reverse

# Models

class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    # The slug field generates all the urls of our model automatically
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    # self - instance of our model 
    def get_url(self):
        # Redirecting the user to the url according to the given category
        # We use reverse because we're redirecting the user to another url
        return reverse('store_app:products_by_category', args=[self.slug])

    def __str__(self):
        return self.category_name