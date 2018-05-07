from rest_framework.viewsets import GenericViewSet
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.decorators import action
from rest_framework.response import Response


class UserViewSet(GenericViewSet):
    @action(detail=False)
    def qq_login(self, request, *args, **kwargs):
        ac_code = request.GET.get("code", None)
        if not ac_code:
            return Response(status=504)


class UserHtmlViewSet(GenericViewSet):
    renderer_classes = (TemplateHTMLRenderer,)

    @action(detail=False)
    def home(self, request, *args, **kwargs):
        return Response(template_name="index1.html")

    @action(detail=False)
    def user_login(self, request, *args, **kwargs):
        return Response(template_name="user_login.html")
