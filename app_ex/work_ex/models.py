from app_ex.user_ex.models import User
from django.db import models
from django.conf import settings


class Lottery(models.Model):
    # 抽奖
    title = models.CharField(max_length=225)
    content = models.TextField()
    # 发布人
    sponsor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 是否匿名
    anonymous = models.BooleanField(default=False)
    # 参与者
    participant = models.ManyToManyField(settings.AUTH_USER_MODEL)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    ended = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)


class Prize(models.Model):
    # 奖品
    name = models.CharField(max_length=225)
    number = models.IntegerField()
    lottery = models.ForeignKey(Lottery, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)


class WinningInfo(models.Model):
    lottery = models.ForeignKey(Lottery, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
