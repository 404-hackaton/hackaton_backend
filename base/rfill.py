from models import *
from random import *
from russian_names import RussianNames
from transliterate import translit
from random import random
from django.http import JsonResponse
from django.db import models
def rfill(times):
    for _ in range(times):
        first_name, surname, last_name = RussianNames().get_person().split()
        email = translit(last_name, "ru", reversed=True) + "." + translit(first_name[0], "ru", reversed=True) + "." + translit(surname[0], "ru", reversed=True) + "." + translit(surname[0], "ru", reversed=True)
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

        user = User(email=email.lower(), password=password, first_name=first_name, last_name=last_name, surname=surname,
                    role=role, status=True)
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


    profs = User.objects.filter(role = "PROFESSOR")
    if profs.exists():
        alphabet = list("АБВГДЕЖЗИКЛМНОПРСТУФ")
        group_name = choice(alphabet) + choice(alphabet) + choice(["Б", "М", "А"]) + choice(["О", "З"]) + "-" + str(randrange(1, 20)) + "-" + str(randrange(19, 25))
        new_group = Group(group_name = group_name, professor = choice(profs))
        new_group.save()
    del profs

    students = User.objects.filter(role_exact = "STUDENT")
    groups = Group.object.values_list('group_name', flat=True)
    if students.exists() and groups.exists():
        stud_in_group = GroupMember.objects.values('student')
        ranstud = choice(students)
        while(ranstud in stud_in_group):
            ranstud = choice(students)
        new_member = GroupMember(group = choice(groups), student = ranstud)
        new_member.save()
        del stud_in_group
    del groups

    courses = Course.objects.all()
    if students.exists() and courses.exists():
        grade = 0
        gr_type = choice(['attendance', 'activities', 'achievments', 'test'])
        match gr_type:
            case 'attendance':
                grade = randrange(0, 16)
            case 'activities':
                grade = randrange(0, 4)
            case 'achievments':
                grade = choice([randrange(0, 6), 100]) # за участие могут дать автомат, помните?
            case 'test':
                grade = randrange(0, 6)
        subj = choice(Schedule.objects.all())
        new_grade = Grade(student = choice(students), course = choice(courses), grade = grade, grade_type = gr_type, source = subj)
        new_grade.save()
        del courses

    subjects = Schedule.objects.all()
    if students.exists() and subjects.exists():
        new_attendance = Attendence(student = choice(students), source = choice(subjects), status = choice(['Н', 'У', '+']))
        new_attendance.save()
    del subjects
    del students





    return JsonResponse({"status": 200})
