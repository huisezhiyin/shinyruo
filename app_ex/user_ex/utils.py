from rest_framework.authentication import BaseAuthentication
from app_ex.user_ex.models import Token, User
from rest_framework import exceptions
from django.conf import settings
import datetime
import binascii
import requests
import json
import os
import re


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


class QQLogin(object):
    qq_token_url = settings.QQ_TOKEN_URL
    qq_open_id_url = settings.QQ_OPEN_ID_URL
    app_conf = settings.QQ_APP_CONF
    # todo:此处到时候需要改成域名
    token_callback = "http://45.40.196.121/users/qq_login/"
    grant_type = "authorization_code"

    def token(self, ac_code):
        app_id = self.app_conf["app_id"]
        app_key = self.app_conf["app_key"]
        url_token = "{0}/token?client_id={1}&client_secret={2}&code={3}&grant_type={4}&redirect_uri={5}".format(
            self.qq_token_url, app_id, app_key, ac_code, self.grant_type, self.token_callback, )
        response_token = requests.get(url_token).content
        response_dict = dict(i.split("=") for i in response_token.split("&"))
        return response_dict

    def open_id(self, ac_code):
        token_dict = self.token(ac_code)
        access_token = token_dict["access_token"]
        url_me = "{0}/?access_token={1}".format(self.qq_open_id_url, access_token)
        response_open_id = requests.get(url_me).content
        open_id_dict = json.loads(re.search(r'callback\((.+?)\)', response_open_id).group(1))
        open_id = open_id_dict["openid"]
        return open_id
