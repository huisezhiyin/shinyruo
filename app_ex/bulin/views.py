from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from app_ex.work_ex.models import Lottery, Prize
from django.http import HttpResponse


class BulinViewSet(GenericViewSet):
    pass
