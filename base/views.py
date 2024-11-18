from django.http import JsonResponse
from .models import *
from random import random
import datetime
import random


COURSE_TIME = {
    "1": "09:00",
    "2": "10:40",
    "3": "12:40",
    "4": "14:20",
    "5": "16:20",
    "6": "18:00",
}

def mktk(): #MaKe ToKen
    alphabet = list("0123456789ABCDEFGHIJKOPQRSTUVWXVZabcdefgijkopqrstuvwxyz!_+-&?")
    Token = ""
    for i in range(10):
        Token += random.choice(alphabet)
    return Token

def home(request):
    users = User.objects.all()
    users_dict = {}
    for user in users:
        users_dict[user.email] = user.password
    return JsonResponse(users_dict)

def proc(request):
    req_type = request.META["TYPE"]
    if ((req_type != "LOG_IN") and (req_type != "REGIST")): #если это не запрос регистрации/входа в ситему - время проверки токена!
        connect_token = request.META["TOKEN"]
        exists = Token.objects.filter(user_token=connect_token).exists()
        if not exists:
            JsonResponse({"STATUS": 401}) #если такого токена нет, кидаем Максу JSON с неавторизацией
        else:
            corr = True

    elif (req_type == "LOG_IN"):
        connect_password = request.META["PASSWORD"]
        connect_login = request.META["LOGIN"]
        users_by_login = User.objects.filter(email=login)
        corr = False
        ind = 0
        if users_by_login.exists() and users_by_login[0].password == connect_password:
            corr = True
        if not corr:
            JsonResponse({"STATUS": 404}) # И какой код мне ему вернуть? 404, типо такой учетки нет, или 401 с пояснением? Пока оставлю 404
        else:
            user = User.objects.get(email_exact=connect_login)

            user_data(request, user.get_id())

    elif req_type == "REGIST":
        connect_password = request.META["PASSWORD"]
        connect_login = request.META["LOGIN"]
        connect_fn = request.META["FIRST_NAME"]
        connect_ln = request.META["LAST_NAME"]
        connect_sn = request.META["SURNAME"]
        new_user = User(email = connect_login, password = connect_password, first_name = connect_fn, last_name = connect_ln, surname = connect_sn, role = "STUDENT") #Условимся что роль по-умолчанию  - студент, более высокие роли пусть дают админы
        new_user.save()
        user = User.objects.get(emai_exact = connect_login)
        tokens = Token.objects.values_list('user_token', flat=True)
        conn_token = mktk()
        while conn_token in tokens:
            conn_token = mktk()
        del tokens
        new_token = Token(user_token=conn_token, user_id= user.get_id())
        new_token.save()

def user_data(request, user_id):
    user = User.objects.get(id=user_id)
    user_group_id = None if len(user.get_group_id()) == 0 else user.get_group_id()[0]["group_id"]
    user_token = Token(user_id_exact = user_id)
    print(user_group_id)
    data = {
        "email": user.email,
        "first_name": user.first_name.encode('unicode-escape').decode('unicode-escape'),
        "last_name": user.last_name.encode('unicode-escape').decode('unicode-escape'),
        "surname": user.surname.encode('unicode-escape').decode('unicode-escape'),
        "role": user.role,
        "group_id": user_group_id,
        "TOKEN":user_token.user_token.encode('unicode-escape').decode('unicode-escape')
        }
    return JsonResponse(data)

def user_group_members(request, user_id):
    members = User.objects.get(id=int(user_id)).get_all_group_members()
    return JsonResponse({"users": [member.email for member in members]})


def schedule_day(request, user_id, date):
    schedules = User.objects.filter(id=user_id)[0].get_schedule_day(date=date)
    schedules_data = {"schedules": []}
    for schedule in schedules:
        schedules_data["schedules"].append((
            {"course_name": schedule.course.course_name},
            {"course_type": schedule.course.course_type},
            {"professor": f"{schedule.professor.first_name} {schedule.professor.last_name} {schedule.professor.surname}"},
            {"audience": schedule.audience},
            {"location": schedule.location},
            {"date_year": str(schedule.date)[:4]},
            {"date_month": str(schedule.date)[5:7]},
            {"date_day": str(schedule.date)[8:]},
            {"time_hour": COURSE_TIME[schedule.time][:2]},
            {"time_minute": COURSE_TIME[schedule.time][3:]},
            {"groups": [group.group_name for group in schedule.groups.all()]},
        ))
    print(schedules_data)
    return JsonResponse(schedules_data)



#TODO: Придумать другой способ искать конкретную строку по логину. Перебирать всю базу данных - беспощадно к памяти
#TODO: Дописать регистрацию токена
