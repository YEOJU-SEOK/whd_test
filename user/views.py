#from django.shortcuts import render
import json, bcrypt, re, jwt

from datetime import datetime, timedelta
from django.views import View
from django.http import JsonResponse

from my_settings import SECRET, ALGORITHM
from .models import User, Gender
from .utils import login_auth

class SignUpView(View):

    def validate_email(self, email):
        REGEX_EMAIL = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(REGEX_EMAIL, email)

    def validate_password(self, password):
        REGEX_PASSWORD = '^[a-zA-Z0-9!@#$%^&*+=]{2,16}$'

        return re.match(REGEX_PASSWORD, password)

    def validate_number(self, number):
        REGEX_NUMBER = '^[0-9]{11}$'

        return re.match(REGEX_NUMBER, number)

    def post(self,request):
        data = json.loads(request.body)
        try:
            if not self.validate_email(data['email']):
                return JsonResponse({"message":"INVALID_EMAIL"}, status=401)
            if not self.validate_password(data['password']):
                return JsonResponse({"message":"INVALID_PASSWORD"}, status=401)
            if not self.validate_number(data['number']):
                return JsonResponse({"message":"INVALID_NUMBER"}, status=401)
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({"message":"USER_EXIST"}, status=409)
            if User.objects.filter(number=data['number']).exists():
                return JsonResponse({"message":"NUMBER_EXIST"}, status=409)

            hashed_pw = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode()

            User.objects.create(
                email = data['email'],
                password = hashed_pw,
                number = data['number'],
                gender_id = Gender.objects.get(name=data['gender']).id
            )
            return JsonResponse({"message":"SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"},status=401)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if not User.objects.filter(email=data['email']).exists():
                return JsonResponse({"message":"INVALID_USER"}, status=401)
            if not bcrypt.checkpw(data['password'].encode('utf-8'), User.objects.get(email=data['email']).password.encode('utf-8')):
                return JsonResponse({"message":"INVALID_PASSWORD"}, status=401)
            #accesstoken decode...뭐지?
            access_token = jwt.encode({'id':User.objects.get(email=data['email']).id, 'exp': datetime.now() + timedelta(hours=24)}, SECRET, ALGORITHM).decode('utf-8')
            return JsonResponse({"message":"SUCCESS", "TOKEN":access_token}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"message":"FAILDED_TO_DECODE_DATA"}, status=400)
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=403)