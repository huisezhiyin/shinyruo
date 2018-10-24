from rest_framework.viewsets import GenericViewSet
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http.response import HttpResponseRedirect
from django.contrib.auth import login
from app_ex.user_ex.models import OAuth, User
from app_ex.user_ex.utils import QQOAuth
import binascii
import time
import os


class UserHtmlViewSet(GenericViewSet):
    renderer_classes = (TemplateHTMLRenderer,)

    @action(methods=["GET"], detail=False)
    def home(self, request, *args, **kwargs):
        return Response(template_name="index1.html")

    @action(methods=["GET"], detail=False)
    def user_login(self, request, *args, **kwargs):
        return Response(template_name="user_login.html")


class UserViewSet(GenericViewSet):
    qq_oauth = QQOAuth()

    @action(methods=["GET"], detail=False)
    def qq_login(self, request, *args, **kwargs):
        callback_encode = "https%3a%2f%2fshinyruoqaq.cn%2fusers%2fqq_callback"
        url_base = "https://graph.qq.com/oauth2.0/authorize"
        app_id = self.qq_oauth.app_id
        state = "qq_{0}".format(int(time.time() * 1000))
        url = f"{url_base}?response_type=code&client_id={app_id}&redirect_uri={callback_encode}&state={state}"
        return HttpResponseRedirect(redirect_to=url)

    @action(methods=["GET", "POST"], detail=False)
    def qq_callback(self, request, *args, **kwargs):
        ac_code = request.GET.get("code", None)
        if not ac_code:
            return Response(status=504)
        user = self.__qq_login__(ac_code)
        login(request, user)
        return HttpResponseRedirect(redirect_to="/lottery_home/home/")

    def __qq_login__(self, ac_code):
        open_id_dict = self.qq_oauth.open_id(ac_code)
        open_id = open_id_dict.get("open_id")
        access_token = open_id_dict.get("access_token")
        user_info = self.qq_oauth.user_info(access_token, open_id)
        head_image_url = user_info.get("figureurl_qq_2") or user_info.get("figureurl_qq_1")
        sex = user_info.get("gender")
        nickname = user_info.get("nickname")
        sex_dict = {"男": 1, "女": 2}
        sex = sex_dict.get(sex) or 0

        try:
            oauth = OAuth.objects.get(platform=OAuth.QQ, open_id=open_id)
            user = oauth.user
            user.nickname = nickname
            user.sex = sex
            user.avatar_url = head_image_url
            user.save()
        except OAuth.DoesNotExist:
            user = User.objects.create_user(
                nickname=nickname,
                sex=sex,
                avatar_url=head_image_url,
            )
            oauth = OAuth.objects.create(
                user=user,
                platform=OAuth.QQ,
                open_id=open_id,
                access_token=binascii.hexlify(os.urandom(20)).decode()
            )
        return user
