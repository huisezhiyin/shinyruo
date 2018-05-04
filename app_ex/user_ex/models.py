from django.contrib.auth.models import AbstractUser, Group
from django.utils.translation import gettext_lazy as _
from django.db import models


class User(AbstractUser):
    OTHER = 0
    MAN = 1
    WOMAN = 2
    SEX_CHOICE = (
        (OTHER, "其他"),
        (MAN, "男"),
        (WOMAN, "女")
    )
    nickname = models.CharField(_('nickname'), max_length=255)
    sex = models.IntegerField(default=OTHER, choices=SEX_CHOICE)
    avatar_url = models.CharField(max_length=1024, null=True)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    mask = models.BooleanField(default=True)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
