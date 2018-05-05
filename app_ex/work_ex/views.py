from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from app_ex.work_ex.models import Lottery, Prize
from django.http import HttpResponse


# Create your views here.
def hello(request):
    return HttpResponse("hello shinyruo")


class LotteryViewSet(GenericViewSet):

    pass
