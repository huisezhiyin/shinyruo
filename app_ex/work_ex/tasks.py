from app_ex.repeater.utils import RandomNumber
from app_ex.work_ex.models import Lottery, Prize, WinningInfo
from app_ex.user_ex.models import User
from django.db.models import Sum
from shinyruo_qaq.celery import app
import datetime
import heapq


@app.task(bind=True)
def lottery_task(self,lottery_id):
    try:
        lottery = Lottery.objects.get(id=lottery_id)
    except Lottery.DoesNotExist:
        return -4
    if lottery.ended:
        return -2
    lottery.ended = True
    lottery.save()
    winner_list = []
    participant_list = lottery.participant.all()
    # 获取所有奖品数
    prize_queryset = Prize.objects.filter(lottery=lottery)
    prize_number = prize_queryset.aggregate(Sum("number"))["number__sum"]
    if prize_number <= len(participant_list):
        random_number = RandomNumber()
        result_list = random_number.random_number(len(participant_list), prize_number)
        for i in result_list:
            winner_list.append(participant_list[i])
    else:
        winner_list = participant_list
    # 按顺序写入奖品 这样做比较粗燥
    # 当winner list无法互相比较的时候是无法压入堆的
    winner_list = heapq.heapify(winner_list)
    for prize in prize_queryset:
        for i in range(prize.number):
            win = WinningInfo.objects.create(
                lottery=lottery,
                user=heapq.heappop(winner_list),
                prize=prize
            )
    return 1
