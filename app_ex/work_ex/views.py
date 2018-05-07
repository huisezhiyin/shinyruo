from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from app_ex.work_ex.models import Lottery, Prize
from django.http import HttpResponse


# Create your views here.
def hello(request):
    return HttpResponse("hello shiny_ruo")


class LotteryViewSet(GenericViewSet, mixins.ListModelMixin):
    queryset = Lottery.objects.filter(ended=False)
    pagination_class = PageNumberPagination


class LotteryHtmlViewSet(GenericViewSet):
    renderer_classes = (TemplateHTMLRenderer,)

    @action(detail=False)
    def home(self, request, *args, **kwargs):
        return Response(template_name="index1.html")
