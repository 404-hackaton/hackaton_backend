from django.http import JsonResponse
from .models import *


def home(request):
    users = User.objects.all()
    users_dict = {}
    for user in users:
        users_dict[user.email] = user.password

        print(user.group_memberships.values('group_id'))
        # print(user.get_all_group_members())
    return JsonResponse(users_dict)


def user_data(request, user_id):
    user = User.objects.get(id=user_id)
    user_group_id = None if len(user.get_group_id()) == 0 else user.get_group_id()
    print(user_group_id)
    data = {
        "email": user.email,
        "first_name": user.first_name.encode("UTF-8").decode(),
        "last_name": user.last_name,
        "surname": user.surname,
        "role": user.role,
        "group_id": user_group_id
        }
    return JsonResponse(data)

def user_group_members(request, user_id):
    members = User.objects.get(id=int(user_id)).get_all_group_members()
    return JsonResponse({"users": [member.email for member in members]})


# def schedule_day(request, date, user):

    

