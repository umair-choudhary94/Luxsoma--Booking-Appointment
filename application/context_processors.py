from .models import Category
def services(request):
    # Retrieve the services
    categories = Category.objects.all()
    
    # Return a dictionary containing the services
    return {'categories': categories}
