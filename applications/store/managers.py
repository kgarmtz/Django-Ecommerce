from django.db import models

class VariationManager(models.Manager):
    # Returns all the color variations from a specific product
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)
   # Returns all the size variations from a specific product
    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)