# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

# 备忘：数据库更新命令：
# $ python manage.py makemigrations
# $ python manage.py migrate


class User(AbstractUser):
    nickname = models.CharField(max_length=50)
    point=models.IntegerField(default=0)
    class Meta(AbstractUser.Meta):
        verbose_name = '用户'
        verbose_name_plural = '用户'
        pass

