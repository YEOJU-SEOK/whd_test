#from django.shortcuts import render
import json, bcrypt, re, jwt

from datetime import datetime, timedelta
from django.views import View
from django.http import JsonResponse

from my_settings import SECRET, ALGORITHM
from user.models import User, Gender, Address
from user.utils import login_auth


#회원가입
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


#로그인
class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if not User.objects.filter(email=data['email']).exists():
                return JsonResponse({"message":"INVALID_USER"}, status=401)
            if not bcrypt.checkpw(data['password'].encode('utf-8'), User.objects.get(email=data['email']).password.encode('utf-8')):
                return JsonResponse({"message":"INVALID_PASSWORD"}, status=401)

            access_token = jwt.encode({'id':User.objects.get(email=data['email']).id, 'exp': datetime.now() + timedelta(hours=24)}, SECRET, ALGORITHM)
            print(access_token)
            print("type:", type(access_token))
            return JsonResponse({"message":"SUCCESS", "TOKEN":access_token}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"message":"FAILDED_TO_DECODE_DATA"}, status=400)
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=403)

#정보조회&업데이트
class UserView(View):
    @login_auth
    def get(self, request):
        user = request.user    
        if not user:
            return JsonResponse({"mesage":"USER_NOT_FOUND"}, status=404)
        result = [{
            'email' : user.email,
            'number' : user.number,
            'gender' : user.gender.name
        }]
        return JsonResponse({'message':'SUCCESS', 'results': result}, status=200)

    @login_auth
    def patch(self, request, user_id):
        user = request.user
        try:
            if User.objects.filter(id=user_id):
                user = User.objects.get(id=user_id)
                
                user.number = data.get('number', user.number)
                user.gender = data.get('gender', user.gender)
                
                user.save()
                return JsonResponse({"message" : "SUCCESS"}, status=201)

            return JsonResponse({"message" : "INVALID_APPROACH"}, status=400)       

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)         