from django.db import models


class Lottery(models.Model):
    # 抽奖
    title = models.CharField(max_length=225)
    content = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)


class Prize(models.Model):
    # 奖品
    name = models.CharField(max_length=225)
    number = models.IntegerField()
    lottery = models.ForeignKey(Lottery, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
