import asyncio
import datetime
import json
import base64
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from .models import Thread,ChatMessage

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        print("connected",event)
        other_user=self.scope['url_route']['kwargs']['username']
        me=self.scope['user']
        thread_obj=await self.get_thread(me,other_user)
        self.thread_obj=thread_obj
        chat_room=f"thread_{thread_obj.id}"
        self.chat_room=chat_room
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )
        await self.send({
            "type":"websocket.accept"
        })
        other_user=self.scope['url_route']['kwargs']['username']
        me=self.scope['user']
        thread_obj=await self.get_thread(me,other_user)
        chat_room=f"thread_{thread_obj.id}"
        self.chat_room=chat_room

    async def websocket_receive(self,event):
        front_text=event.get('text',None)
        data=None
        imageid=1
        ext=''
        if front_text is not None:
            loaded_dict_data=json.loads(front_text)
            msg=loaded_dict_data['message']
            if loaded_dict_data['image']!=1:
                imageid=str(datetime.datetime.now())
                img=loaded_dict_data['image']
                fmat,imgstr=img.split(';base64,')
                ext=fmat.split('/')[-1]
                data=ContentFile(base64.b64decode(imgstr),name=f"{imageid}"+'.'+ext)
                imageid += '.' + ext
                imageid =imageid.replace(' ','_')
                imageid=imageid.replace(':','')
            user=self.scope['user']
            username='guest'
            if user.is_authenticated:
                username=user.username
            resp={
                'message':msg,
                'image':imageid,
                'username':username
            }
            await self.create_new_chat_msg(msg,data)
            #broadcasts the message event to be sent
            await self.channel_layer.group_send(
                self.chat_room,
                {
                    "type":"chat_message",
                    "text":json.dumps(resp)
                }
            )

    async def chat_message(self,event):
        #sends the actual msg
        await self.send({
            "type":"websocket.send",
            "text":event['text']
        })

    async def websocket_disconnect(self, event):
            print("disconnected", event)

    @database_sync_to_async
    def get_thread(self,user,other_username):
        return Thread.objects.get_or_new(user,other_username)[0]

    @database_sync_to_async
    def create_new_chat_msg(self,msg,img=None):
        thread_obj=self.thread_obj
        me=self.scope['user']
        return ChatMessage.objects.create(thread=thread_obj,user=me,message=msg,image=img)