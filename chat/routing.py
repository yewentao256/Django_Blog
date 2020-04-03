# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    # ?P表示命名一个room_name的组，匹配规则符合后面的\w
    # \w 匹配字母或数字或下划线或汉字 等价于 '[^A-Za-z0-9_]'，+匹配至少一个字符
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer),
]