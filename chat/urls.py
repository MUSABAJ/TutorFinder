from django.urls import path
from . import views
urlpatterns = [

    path('', views.chat_rooms, name='chat_rooms'),
    path('room/<int:chat_id>', views.room, name='room'),
    path('room/send/<int:chat_id>', views.send_message, name='send_msg'),
    path('room/get/<int:chat_id>', views.get_messages, name='get_msgs'),
    # path('new_chat/<int:id>', views.get_or_create_chat,name='new_chat')
    path('chats',views.chats,name='chats'),

]
