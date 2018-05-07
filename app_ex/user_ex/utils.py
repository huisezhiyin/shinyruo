from rest_framework.authentication import BaseAuthentication
from app_ex.user_ex.models import Token, User
from rest_framework import exceptions
import datetime
import binascii
import os


# 通过用户获取token的函数
def user_token(user):
    if not isinstance(user, User):
        raise exceptions.AuthenticationFailed("user is not User isinstance")
    try:
        token = Token.objects.get(user=user)
        if token.expired_time < datetime.datetime.now():
            token.key = binascii.hexlify(os.urandom(20)).decode()
            token.expired_time = datetime.datetime.now() + datetime.timedelta(days=30)
            token.save()
    except Token.DoesNotExist:
        token = Token.objects.create(
            user=user,
            client_type=Token.OTHER, )
    return {"code": 0, "token": token.key, "expired_time": token.expired_time}


# 通过token获取user的装饰器
def token_to_user_decorators(wrapper):
    def auth(self, request, *args, **kwargs):
        key = request.META.get("HTTP_TOKEN")
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')
        request.user = token.user
        return wrapper(self, request, *args, **kwargs)

    return auth


# 通过token获取user的Authentication类
class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        key = request.META.get("HTTP_TOKEN")
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return (token.user, key)
