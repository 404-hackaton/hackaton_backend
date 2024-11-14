from django.http import JsonResponse
from .models import Users


def home(request):
    print(Users.objects)
    return JsonResponse({'user': 'admin'})
