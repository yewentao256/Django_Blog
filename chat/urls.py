# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    # 进入聊天室
    path('', views.enter, name='enter'),
    # 聊天室界面，这样可以解析room_name，直接做字符串保持
    path('<str:room_name>/', views.room, name='room'),
    # 个人所有信息界面
    # path('contact/', views.contact, name='all_contact'),
    # 个人私聊界面
    path('contact/<str:user1_name>/<str:user2_name>', views.contact, name='contact'),
]
