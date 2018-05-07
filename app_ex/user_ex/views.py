from rest_framework.viewsets import GenericViewSet
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.decorators import action
from rest_framework.response import Response
from app_ex.user_ex.utils import QQOauth


class UserViewSet(GenericViewSet):
    qq_oauth = QQOauth()

    @action(detail=False)
    def qq_login(self, request, *args, **kwargs):
        ac_code = request.GET.get("code", None)
        if not ac_code:
            return Response(status=504)
        open_id = self.qq_oauth.open_id(ac_code)
        #todo:此处进行用户创建/登录



class UserHtmlViewSet(GenericViewSet):
    renderer_classes = (TemplateHTMLRenderer,)

    @action(detail=False)
    def home(self, request, *args, **kwargs):
        return Response(template_name="index1.html")

    @action(detail=False)
    def user_login(self, request, *args, **kwargs):
        return Response(template_name="user_login.html")
