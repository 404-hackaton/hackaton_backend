from django.http import JsonResponse
from .models import *
from random import random
import datetime
import random

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


def schedule_day(request, date, user_id):
    schedules = User.objects.filter(id=user_id)[0].get_schedule_day(date=date)
    schedules_data = {"schedules": ()}
    for schedule in schedules:
        schedules_data["schedules"] = (
            {"course_name": schedule.course.course_name}
        )
    return JsonResponse(schedules_data)

def filling_database(request):
    from russian_names import RussianNames
    from transliterate import translit
    from random import random


    users_count = 20

    # creating users
    for _ in range(users_count):
        first_name, surname, last_name = RussianNames().get_person().split()
        email = translit(last_name, "ru", reversed=True) + "." + translit(first_name[0], "ru", reversed=True) + "." + translit(surname[0], "ru", reversed=True)
        email = email.replace("'", "")
        password = email.lower() + "123123"
        email = email.lower() + "@education.com"
        rand = random()
        if rand < 0.82:
            role = "STUDENT"
        elif rand >= 0.82 and rand < 0.88:
            role = "CAPTAIN"
        elif rand >= 0.88 and rand < 0.95:
            role = "PROFESSOR"
        else:
            role = "ADMINISTRATOR"
        
        user = User(email=email.lower(), password=password, first_name=first_name, last_name=last_name, surname=surname, role=role, status=True)
        user.save()
    
    # adding courses
    creating_courses = False
    courses_data = (
        ("Информатика", "Практика", "Кафедра информатики"),
        ("Информатика", "Лекция", "Кафедра информатики"),
        ("Основы российской государственности", "Практика", "Кафедра гуманитарных и социальных наук"),
        ("Основы российской государственности", "Лекция", "Кафедра гуманитарных и социальных наук"),
        ("История России", "Практика", "Кафедра гуманитарных и социальных наук"),
        ("История России", "Лекция", "Кафедра гуманитарных и социальных наук"),
        ("Введение в профессиональную деятельность", "Практика", "Кафедра индустриального программирования"),
        ("Введение в профессиональную деятельность", "Лекция", "Кафедра индустриального программирования"),
        ("Математический анализ", "Практика", "Кафедра высшей математики-3"),
        ("Математический анализ", "Лекция", "Кафедра высшей математики-3"),
        ("Технологии индустриального программирования", "Практика", "Кафедра индустриального программирования"),
        ("Технологии индустриального программирования", " Лекция", "Кафедра индустриального программирования"),
        ("Иностранный язык", "Практика", "Кафедра иностранных языков"),
    )
    if creating_courses:
        for course_name, course_type, institute in courses_data:
            course = Course(course_name=course_name, course_type=course_type, institute=institute)
            course.save()

    
    

    return JsonResponse({"status": 200})



#TODO: Придумать другой способ искать конкретную строку по логину. Перебирать всю базу данных - беспощадно к памяти
#TODO: Дописать регистрацию токена
