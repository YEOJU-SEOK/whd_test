import jwt

from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from my_settings import SECRET, ALGORITHM
from user.models import User, Gender

def login_auth(func):
    def wrapper(self, request, *args, **kargs):
        #Authorization 없는경우
        if "Authorization" is None:
            return JsonResponse({"message":"INVALID_TOKEN"}, status=401)

        #있으면? 토큰을 정의하고
        encode_token = request.headers["Authorization"]
        try:
            data = jwt.decode(encode_token, SECRET, ALGORITHM)
            user = User.objects.get(id=data["id"])
            request.user = user
            return self.func(self, request, *args, **kargs)

        except jwt.DecodeError:
            return JsonResponse({"message":"DECODE_ERROR"}, status=401)
        except User.DoesNotExist:
            return JsonResponse({"message":"INVALID_USER"}, satatus=401)
        except jwt.ExpiredSignatureError:
            return JsonResponse({"message":"EXPIRED_TOKEN"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"message":"INVALID_TOKEN"}, status=401)
    return wrapper
