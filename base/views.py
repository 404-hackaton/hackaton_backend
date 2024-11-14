from django.http import JsonResponse
from .models import User


def home(request):
    print(User.objects)
    return JsonResponse({'user': 'admin'})
