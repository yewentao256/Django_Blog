# chat/views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import Contact


@login_required
# 进入聊天室界面
def enter(request):
    return render(request, 'chat/enter.html', {})


@login_required
# 聊天室界面，room_name是作为url解析传进来的
def room(request, room_name):
    return render(request, 'chat/room.html', {'room_name': room_name})


@login_required
# 个人私聊界面
def contact(request, user1_name, user2_name):
    user1 = User.objects.get(username=user1_name)
    user2 = User.objects.get(username=user2_name)
    if Contact.objects.filter(user1=user1, user2=user2) or Contact.objects.filter(user1=user2, user2=user1):
        pass
    else:
        Contact.objects.create(user1=user1, user2=user2, log="")
    return render(request, 'chat/contact.html', {'user1': user1_name, 'user2': user2_name})
