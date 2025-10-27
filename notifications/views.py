# notifications/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,  get_object_or_404
from .models import Notification

@login_required
def notification_list(request):
    notifications = request.user.notifications.all()
    return render(request, 'notifications/list.html', {'notifications': notifications})

@login_required
def mark_notification_read(request, notif_id):
    notif = get_object_or_404(Notification, id=notif_id, recipient=request.user)
    notif.mark_as_read()
    return redirect(notif.link or 'notification_list')
