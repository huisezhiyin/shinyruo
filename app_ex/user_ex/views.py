from rest_framework.viewsets import GenericViewSet
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.decorators import action
from rest_framework.response import Response
from app_ex.user_ex.models import OAuth, User
from app_ex.user_ex.utils import QQOAuth, user_token
import binascii
import os


class UserHtmlViewSet(GenericViewSet):
    renderer_classes = (TemplateHTMLRenderer,)

    @action(detail=False)
    def home(self, request, *args, **kwargs):
        return Response(template_name="index1.html")

    @action(detail=False)
    def user_login(self, request, *args, **kwargs):
        return Response(template_name="user_login.html")


class UserViewSet(GenericViewSet):
    qq_oauth = QQOAuth()

    @action(detail=False)
    def qq_login(self, request, *args, **kwargs):
        ac_code = request.GET.get("code", None)
        if not ac_code:
            return Response(status=504)
        open_id_dict = self.qq_oauth.open_id(ac_code)
        open_id = open_id_dict.get("open_id")
        access_token = open_id_dict.get("access_token")
        user_info = self.qq_oauth.user_info(access_token, open_id)
        head_image_url = user_info.get("figureurl_qq_2") or user_info.get("figureurl_qq_1")
        sex = user_info.get("gender")
        nickname = user_info.get("nickname")
        # todo:此处进行用户创建/登录
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
        return Response({"key": user_token(user)})

    @action(methods=["GET","POST"])
    def qq_callback(self, request, *args, **kwargs):
        return Response(200)