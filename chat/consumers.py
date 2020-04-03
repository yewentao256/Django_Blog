# chat/consumers.py
import json
from datetime import datetime

from django.utils import timezone
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    # 初始化
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 从scope中获取room_name（实际是从url路由中获取参数）
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        # %s相当于把room_name换进去
        self.room_group_name = 'chat_%s' % self.room_name

    # 加入房间组
    async def connect(self):
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    # 离开房间组
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # 从websocket中接收信息
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_name = text_data_json['user_name']
        # 把消息传给房间组
        await self.channel_layer.group_send(self.room_group_name,
                                            {'type': 'chat_message', 'message': message,'user_name':user_name})

    # 从房间组中接收消息并返回给websocket
    async def chat_message(self, event):
        # time = timezone.now()
        time = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
        message = event['message']
        user_name = event['user_name']
        # 把消息返回给websocket
        await self.send(text_data=json.dumps({'message': message, 'time': time, 'user_name':user_name}))

