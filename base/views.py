from django.http import JsonResponse
from .models import User, Tokens
import random

def mktk(): #MaKe ToKen
    alphabet = list("0123456789ABCDEFGHIJKOPQRSTUVWXVZabcdefgijkopqrstuvwxyz!_+-&?")
    Token = ""
    for i in range(10):
        Token += random.choice(alphabet)
    return Token

def home(request):
    print(User.objects)
    return JsonResponse({'user': 'admin'})

def proc(request):
    req_type = request.META["TYPE"]
    if ((req_type != "LOG_IN") and (req_type != "REGIST")): #если это не запрос регистрации/входа в ситему - время проверки токена!
        connect_token = request.META["TOKEN"]
        created_tokens = Tokens.objects.values_list('user_token', flat = True).distinct() # получаем все существующие токены
        if connect_token not in created_tokens:
            del(created_tokens) # освобождаем память
            JsonResponse({"STATUS": 401}) #если такого токена нет, кидаем Максу JSON с неавторизацией

    elif (req_type == "LOG_IN"):
        connect_password = request.META["PASSWORD"]
        connect_login = request.META["LOGIN"] #полагаю мыло будет логином
        logins = User.objects.values_list('email', flat = True).distinct()
        passwords = User.objects.values_list('password', flat = True).distinct()
        corr = False
        ind = 0
        for login in range(len(logins)):
            if (logins[login] == connect_login) and (passwords[login] == connect_password): #ура оно нашлось
                corr = True
                ind = login #зачем? ниже, при удачной регистрации
                break

        del(logins)
        del(passwords) #освобождаю память
        if not corr:
            JsonResponse({"STATUS": 404}) # И какой код мне ему вернуть? 404, типо такой учетки нет, или 401 с пояснением? Пока оставлю 404

        else:
            first_name = (User.objects.values_list('first_name', flat = True).distinct())[ind]
            last_name = (User.objects.values_list('Last_name', flat = True).distinct())[ind]
            surname = (User.objects.values_list('surname', flat = True).distinct())[ind]
            tokens = Tokens.objects.values_list('user_token', flat = True).distinct()
            conn_token = mktk()
            while conn_token in tokens:
                conn_token = mktk()
            #new_line = Tokens(user_tiken = conn_token, )
            JsonResponse({"NAME": first_name, "LAST_NAME": last_name, "SURNAME": surname, "TOKEN": conn_token})


#TODO: Придумать другой способ искать конкретную строку по логину. Перебирать всю базу данных - беспощадно к памяти
#TODO: Дописать регистрацию токена