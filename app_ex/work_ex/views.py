from app_ex.work_ex.serializers import LotterySerializer, PrizeSerializer, WinningInfoSerializer
from app_ex.work_ex.models import Lottery, Prize, WinningInfo
from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse


class LotteryHtmlViewSet(GenericViewSet):
    renderer_classes = (TemplateHTMLRenderer,)

    @action(detail=False)
    def home(self, request, *args, **kwargs):
        return Response(template_name="index1.html")


def hello(request):
    return HttpResponse("hello shiny_ruo")


class LotteryViewSet(GenericViewSet, mixins.ListModelMixin):
    queryset = Lottery.objects.filter(ended=False)
    pagination_class = PageNumberPagination

    @action(detail=False)
    def lottery(self, request, *args, **kwargs):
        queryset = self.queryset
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = LotterySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = LotterySerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def prize(self, request, *args, **kwargs):
        # 获取所有奖品信息
        instance = self.get_object()
        queryset = Prize.objects.filter(lottery=instance)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = PrizeSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = PrizeSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def winning_info(self, request, *args, **kwargs):
        # 此抽奖的获奖信息
        instance = self.get_object()
        if not instance.ended:
            return Response({"code": 1, "msg": "抽奖未完成"})
        queryset = WinningInfo.objects.filter(lottery=instance)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = WinningInfoSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = WinningInfoSerializer(queryset, many=True)
        return Response(serializer.data)
    # todo:发布抽奖
    # todo:参与抽奖 将所有参与抽奖的用户汇集到一起
