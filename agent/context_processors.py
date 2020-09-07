from .models import Manufacturer

def sidebar(request):
    
    return{
        'manufacturers': 'manufacturers',
    }
