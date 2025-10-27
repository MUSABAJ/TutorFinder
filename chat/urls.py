from django.urls import path
from . import views
urlpatterns = [
    path('', views.chat_list, name='chat_list'),
    path('chat/<int:chat_id>', views.chat_detail, name='chat_detail'),
    path('new_chat/<int:id>', views.get_or_create_chat,name='new_chat')
]
