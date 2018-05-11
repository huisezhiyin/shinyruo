from django.contrib.auth.models import AbstractUser, Group
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.conf import settings
import datetime
import binascii
import os


class UserManager(BaseUserManager):
    def create_user(self, nickname, sex=None, avatar_url=None, username=None, password=None):
        if not username:
            username = binascii.hexlify(os.urandom(20)).decode()
        if not sex:
            sex = self.model.OTHER
        if not avatar_url:
            avatar_url = ""
        if password:
            user = self.model(
                username=username,
                nickname=nickname,
                sex=sex,
                avatar_url=avatar_url,
            )
            user.set_password(password)
            user.save()
        else:
            user = self.model(
                username=username,
                nickname=nickname,
                sex=sex,
                avatar_url=avatar_url,
                password="{0}".format(binascii.hexlify(os.urandom(20)).decode()),
            )
        user.save(using=self._db)

        return user


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
    objects = UserManager()

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'


class OAuth(models.Model):
    QQ = 1
    PLATFORM_CHOICE = (
        (QQ, "qq"),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    platform = models.IntegerField(default=QQ, choices=PLATFORM_CHOICE)
    access_token = models.CharField(max_length=128, unique=True)
    open_id = models.CharField(max_length=128, unique=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)


class Token(models.Model):
    # token登陆系统
    IPHONE = 1
    ANDROID = 2
    IPAD = 3
    OTHER = 4
    CLIENT_TYPE = (
        (IPHONE, '肾果'),
        (ANDROID, '安卓'),
        (IPAD, 'iPad'),
        (OTHER, 'other'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    client_type = models.IntegerField(default=IPHONE, choices=CLIENT_TYPE)
    key = models.CharField(max_length=40, unique=True)
    expired_time = models.DateTimeField()
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
            self.expired_time = datetime.datetime.now() + datetime.timedelta(days=60)
        return super(Token, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key


class UserReceiptProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    remark = models.TextField(default="")
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
