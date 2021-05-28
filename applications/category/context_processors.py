# Declaring the global variables that we want to display in the whole application
from .models import Category

# Any function that executes a context_processor will have the 'request' 
# parameter and also returns a context dictionary
def categories_list(request):
    # Fetching all the categories from our database 
    categories = Category.objects.all()
    # Return a context dictionary
    return {
        'categories': categories,
    }