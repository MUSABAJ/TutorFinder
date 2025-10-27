from django.shortcuts import render, redirect, get_object_or_404
from .models import Message, Chat, User


def chat_list(request):
    chats = Chat.objects.filter(participants=request.user).order_by('-created_at')
    return render(request, 'chat/chatlist.html', {'chats': chats})

 
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Chat, Message, User


@login_required
def chat_list(request):
    chats = Chat.objects.filter(participants=request.user).order_by('-created_at')
    return render(request, 'chat/chatlist.html', {'chats': chats})


@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    

    if request.user not in chat.participants.all():
        return redirect('chat_list')


    receiver = chat.participants.exclude(id=request.user.id).first()

    if request.method == 'POST':
        message_content = request.POST.get('msg', '').strip()
        if message_content:
            Message.objects.create(
                chat=chat,
                sender=request.user,
                receiver=receiver,
                content=message_content
            )
            if request.headers.get('HX-Request'):
                return render(request, 'chat/partials/message_list.html', {'chat': chat})
            return redirect('chat_detail', chat_id=chat.id)

    messages = chat.messages.all()
    return render(request, 'chat/chat.html', {'chat': chat, 'messages': messages, 'receiver': receiver})


@login_required
def get_or_create_chat(request, id):
    user = get_object_or_404(User, id=id)

    if user == request.user:
        return redirect('chat_list')

    chat = Chat.objects.filter(participants=request.user).filter(participants=user).first()
    if not chat:
        chat = Chat.objects.create()
        chat.participants.add(request.user, user)
        chat.save()

    return redirect('chat_detail', chat_id=chat.id)



 