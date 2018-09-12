from app_ex.work_ex.serializers import LotterySerializer, PrizeSerializer, WinningInfoSerializer
from app_ex.work_ex.models import Lottery, Prize, WinningInfo
from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import TemplateHTMLRenderer
from app_ex.repeater.utils import ShinyRuoPageNumberViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
import datetime


class LotteryHtmlViewSet(GenericViewSet):
    renderer_classes = (TemplateHTMLRenderer,)

    @action(detail=False)
    def home(self, request, *args, **kwargs):
        return Response(template_name="index1.html")


def hello(request):
    return HttpResponse("hello shiny_ruo")


class LotteryViewSet(ShinyRuoPageNumberViewSet):
    queryset = Lottery.objects.filter(ended=False)

    @action(detail=False, methods=["POST"])
    def launcher(self, request, *args, **kwargs):
        title = request.data.get("title")
        content = request.data.get("content")
        anonymous = request.data.get("anonymous", False)
        if anonymous:
            anonymous = True
        else:
            anonymous = False
        start_time = request.data.get("start_time", datetime.datetime.now())
        end_time = request.data.get("end_time", start_time + datetime.timedelta(hours=3))
        if end_time < start_time:
            return Response({"code": -2, "msg": "结束时间不能小于开始时间"})
        sponsor = request.user
        lottery = Lottery.objects.create(
            title=title,
            content=content,
            sponsor=sponsor,
            anonymous=anonymous,
            start_time=start_time,
            end_time=end_time,
            ended=False,
        )
        # 奖品信息
        serializer = LotterySerializer(lottery)
        return Response({"code": 0, "data": serializer.data})

    @action(detail=False, methods=["GET"])
    def lottery(self, request, *args, **kwargs):
        queryset = self.queryset
        return self.page_response(queryset, LotterySerializer)

    @action(detail=True, methods=["GET"])
    def prize(self, request, *args, **kwargs):
        # 获取所有奖品信息
        instance = self.get_object()
        queryset = Prize.objects.filter(lottery=instance)
        return self.page_response(queryset, PrizeSerializer)

    @action(detail=True, methods=["GET"])
    def winning_info(self, request, *args, **kwargs):
        # 此抽奖的获奖信息
        instance = self.get_object()
        if not instance.ended:
            return Response({"code": 1, "msg": "抽奖未完成"})
        queryset = WinningInfo.objects.filter(lottery=instance)
        return self.page_response(queryset, WinningInfoSerializer)

    # todo:参与抽奖 将所有参与抽奖的用户汇集到一起
    @action(detail=True, methods=["GET"])
    def participation(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.ended:
            return Response({"code": -1, "msg": "该抽奖活动已结束"})
        user = request.user
        if not user:
            return Response(status=403)
        instance.participant.add(user)
        instance.save()
        return Response({"code": 0, "msg": "参与成功，请等待开奖"})
