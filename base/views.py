from django.http import JsonResponse
from models import *
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

def verify_tk(request):
    req_type = request.POST["TYPE"]
    if ((req_type != "LOG_IN") and (req_type != "REGIST")): #если это не запрос регистрации/входа в ситему - время проверки токена!
        connect_token = request.POST["TOKEN"]
        exists = Token.objects.filter(user_token=connect_token).exists()
        if not exists:
            JsonResponse({"STATUS": 401}) #если такого токена нет, кидаем Максу JSON с неавторизацией
            return False
        else:
            return True #такой токен есть, работаем дальше

def log_in(request):
    connect_password = request.POST["PASSWORD"]
    connect_login = request.POST["LOGIN"] # получаем основные данные
    users_by_login = User.objects.filter(email=login)
    corr = False
    if users_by_login.exists() and users_by_login[0].password == connect_password: # проверяем логин + пароль
        corr = True
    if not corr:
        JsonResponse({"STATUS": 404}) # И какой код мне ему вернуть? 404, типо такой учетки нет, или 401 с пояснением? Пока оставлю 404
        return False #возвращаем что регистрация пошла не по плану и продолжать выполнение запроса нет смысла
    else:
        user = User.objects.get(email_exact=connect_login)
        user_data(request, user.id) # отправляем Максу данные в JSON
        return True # ура, юзер реален, продолжаем работу в штатном режиме



def regist(request):
    connect_password = request.POST["PASSWORD"]
    connect_login = request.POST["LOGIN"]
    connect_fn = request.POST["FIRST_NAME"]
    connect_ln = request.POST["LAST_NAME"]
    connect_sn = request.POST["SURNAME"]
    new_user = User(email = connect_login, password = connect_password, first_name = connect_fn, last_name = connect_ln, surname = connect_sn, role = "STUDENT") #Условимся что роль по-умолчанию  - студент, более высокие роли пусть дают админы
    new_user.save()
    user = User.objects.get(emai_exact = connect_login)
    tokens = Token.objects.values_list('user_token', flat=True)
    conn_token = mktk()
    while conn_token in tokens:
        conn_token = mktk()
    del tokens
    new_token = Token(user_token=conn_token, user_id= user.id)
    new_token.save()
    JsonResponse({"STATUS": 200})
    return True #регистрация успешна, ура

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


def attendence_status_day(request, user_id, date):
    statuses = attendences = User.objects.filter(id=user_id)[0].get_attendence_day(date=date)
    status_set = set()
    for status in statuses:
        status_set.add(status.status)
    status_set = "/".join(sorted(list(status_set)))
    return JsonResponse({"status_day": status_set})


def attendence_day(request, user_id, date):
    attendences = User.objects.filter(id=user_id)[0].get_attendence_day(date=date)
    attendences_data = {"attendences": []}
    for attendece in attendences:
        attendences_data["attendences"].append((
            {"source": attendece.source.id},
            {"status": attendece.status},
        ))
    return JsonResponse(attendences_data)
    
'''
def mk_grade(request): # функция чтобы ставить отметки
    if verify_tk(request): #проверяем токен
        user_token = request.POST["TOKEN"]
        prof = Token.objects.filter(token_exact = user_token)[0] # получили юзера
        if prof.role != "professor" or user.role != "administrator":
            JsonResponse({"STATUS": 403}) # возвращаем Максу запрет проведения операции
        else:
'''

def gpa_calculate(request, user_id):
    gpa = 0
    student = User.objects.get(id=int(user_id))
    courses = student.get_courses()
    hours_sum = sum(courses.values_list("hours", flat=True))
    for course in courses:
        grades = sum(Grade.objects.filter(student=user_id, course=course).values_list("grade", flat=True))
        gpa += grades * (course.hours / hours_sum)

    return JsonResponse({"gpa": round(gpa, 2)})


# delete later
def fill(request):
    creating_courses = True

    courses_data = (
        ("Информатика", "Практика", "Кафедра информатики", 64),
        ("Информатика", "Лекция", "Кафедра информатики", 16),
        ("Основы российской государственности", "Практика", "Кафедра гуманитарных и социальных наук", 32),
        ("Основы российской государственности", "Лекция", "Кафедра гуманитарных и социальных наук", 16),
        ("История России", "Практика", "Кафедра гуманитарных и социальных наук", 32),
        ("История России", "Лекция", "Кафедра гуманитарных и социальных наук", 32),
        ("Введение в профессиональную деятельность", "Лекция", "Кафедра индустриального программирования", 16),
        ("Математический анализ", "Практика", "Кафедра высшей математики-3", 32),
        ("Математический анализ", "Лекция", "Кафедра высшей математики-3", 32),
        ("Технологии индустриального программирования", "Практика", "Кафедра индустриального программирования", 32),
        ("Технологии индустриального программирования", " Лекция", "Кафедра индустриального программирования", 16),
        ("Иностранный язык", "Практика", "Кафедра иностранных языков", 32),
        ("Правоведение", "Лекция", "Кафедра государственно-правовых дисциплин", 16),
        ("Правоведение", "Практика", "Кафедра государственно-правовых дисциплин", 16),
        ("Физика", "Лекция", "Кафедра физики и технической механики", 32),
        ("Физика", "Практика", "Кафедра физики и технической механики", 32),
        ("Физика", "Лабароторная", "Кафедра физики и технической механики", 16),
        ("Линейная алгебра и аналитическая геометрия", "Практика", "Кафедра высшей математики-3", 32),
        ("Линейная алгебра и аналитическая геометрия", "Лекция", "Кафедра высшей математики-3", 32),
        ("Алгоритмы и структуры данных", "Практика", "Кафедра индустриального программирования", 32),
        ("Алгоритмы и структуры данных", "Лекция", "Кафедра индустриального программирования", 16),
        ("Физическая культура и спорт (семестр 1)", "Практика", "Кафедра Физического воспитания", 32),
    )
    if creating_courses:
        for course_name, course_type, institute, hours in courses_data:
            if not Course.objects.filter(course_name=course_name, course_type=course_type).exists():
                course = Course(course_name=course_name, course_type=course_type, institute=institute)
                course.save()
            course = Course.objects.get(course_name=course_name, course_type=course_type)
            course.hours = hours
            course.save()
    

    # dont work
    creating_directions = False
    if creating_directions:
        direction = Direction.objects.create(direction_code="09.03.02", direction_name="Фуллстек разработка")
        direction.courses.add(course.id for course in Course.objects.all())

    return JsonResponse({1:1})


#TODO: Придумать другой способ искать конкретную строку по логину. Перебирать всю базу данных - беспощадно к памяти
#TODO: Дописать регистрацию токена

