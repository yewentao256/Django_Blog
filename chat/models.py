from django.db import models
from django.contrib.auth.models import User


# 个人私聊
class Contact(models.Model):
    user1 = models.OneToOneField(User, related_name='user1', on_delete=models.CASCADE)
    user2 = models.OneToOneField(User, related_name='user2', on_delete=models.CASCADE)
    log = models.TextField(blank=True, default="")
