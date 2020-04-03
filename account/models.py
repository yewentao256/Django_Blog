from django.contrib.auth.models import User
from django.db import models


# 对自带User类的扩展——详细基础信息（详细信息——用户可以修改的片段）
class UserInfo(models.Model):
    phone = models.CharField(max_length=20, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    school = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    profession = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    aboutme = models.TextField(blank=True)
    photo = models.ImageField(blank=True)

    def __str__(self):
        return "user:{}".format(self.user.username)
