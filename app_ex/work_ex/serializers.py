from app_ex.work_ex.models import Lottery, Prize
from rest_framework import serializers
from app_ex.repeater.serializers import DatetimeField


class LotterySerializer(serializers.ModelSerializer):
    start_time = DatetimeField()
    end_time = DatetimeField()
    created_time = DatetimeField()
    ended = serializers.SerializerMethodField()
    sponsor_name = serializers.SerializerMethodField()

    class Meta:
        model = Lottery
        fields = ('title', 'content', 'start_time', 'end_time', 'ended', 'created_time', 'sponsor_name')

    def get_ended(self, instance):
        if instance.ended:
            return 1
        else:
            return 0

    def get_sponsor_name(self, instance):
        if instance.anonymous:
            return "匿名"
        else:
            return instance.sponsor.nickname


class PrizeSerializer(serializers.ModelSerializer):
    pass

class WinningInfoSerializer(serializers.ModelSerializer):
    pass