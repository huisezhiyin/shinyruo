from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from app_ex.work_ex.models import Lottery, Prize
from django.http import HttpResponse


# Create your views here.
def hello(request):
    return HttpResponse("hello shiny_ruo")


class LotteryViewSet(GenericViewSet):
    pass
