from django.shortcuts import render, redirect, get_object_or_404
from .models import Message, Chat, User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Chat, Message, User


@login_required
def chats(request):
    chats = Chat.objects.filter(participants=request.user).order_by('-created_at')
    return render(request,'chat/chats.html',{'chats': chats})


def chat_rooms(request):
    chats = Chat.objects.filter(participants=request.user).order_by('-created_at')
    return render(request, 'chat/partials/_chat_rooms.html', {'chats': chats})


@login_required
def room_by_user_id(request, user_id):
       other_user = get_object_or_404(User, id=user_id)
       chat = Chat.objects.filter(participants=request.user).filter(participants=other_user).first()
       return redirect('room', chat_id=chat.id)


@login_required
def room(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    chats = Chat.objects.filter(participants=request.user).order_by('-created_at')
    receiver = chat.participants.exclude(id=request.user.id).first()
    messages = Message.objects.filter(chat=chat) 

    if request.user not in chat.participants.all():
        return redirect('chat_list')

    receiver = chat.participants.exclude(id=request.user.id).first()

    messages = chat.messages.all()
    if request.headers.get('HX-Request'):
        return render(request, 'chat/partials/_chat_detail.html', {'chat': chat, 'messages': messages, 'receiver': receiver})

    return render(request,'chat/chats.html', {'chats': chats,'chat':chat, 'messages': messages, 'receiver': receiver})

def send_message(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    receiver = chat.participants.exclude(id=request.user.id).first()

    content = request.POST.get('msg', '').strip()
    if content:
        Message.objects.create(
                chat=chat,
                sender=request.user,
                receiver=receiver,
                content=content
            )
    messages = Message.objects.filter(chat=chat) 
    return render(request, 'chat/partials/_messages.html', {'chat': chat, 'messages': messages, 'receiver': receiver})




def get_messages(request,chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    receiver = chat.participants.exclude(id=request.user.id).first()
    messages = chat.messages.all().order_by('timestamp')
    return render(request, 'chat/partials/_messages.html', {'chat': chat, 'messages': messages, 'receiver': receiver})


def get_or_create_chat(request, id):
    user = get_object_or_404(User, id=id)
    chat = Chat.objects.filter(participants=request.user).filter(participants=user).first()

    if not chat:
        chat = Chat.objects.create()
        chat.participants.add(request.user, user)
        return redirect('room', chat_id=chat.id)

    return redirect('room', chat_id=chat.id)
