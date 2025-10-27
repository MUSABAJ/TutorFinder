from django.db import models
from users.models import User


class Chat(models.Model):
    participants = models.ManyToManyField(User, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
        names = ", ".join([user.username for user in self.participants.all()])
        return f"Chat between {names}"
    
    def last_message(self):
        return self.messages.order_by('-timestamp').first()


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering= ['timestamp']
        
    def __str__(self):
        return f"{self.sender.username}: {self.content[:30]}"


