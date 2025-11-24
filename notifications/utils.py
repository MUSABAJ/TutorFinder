# notifications/utils.py
import requests
from django.conf import settings
from .models import Notification

# --------------- TELEGRAM UTILS --------------- #

def send_telegram_message(chat_id, text):
    """Send a Telegram message to a specific chat_id."""

    if not chat_id:
        return False  # user hasn't linked Telegram

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
    }


    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
 
        return True
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Telegram message failed: {e}")
        return False


# --------------- NOTIFICATION LOGIC --------------- #

NOTIFICATION_MESSAGES = {
    'session_request': "📩 You have a new session request from @{username}. please respond to the request as soon as posiible ",
    'session_cancel': "❌  @{username} has canceld a Session .",
    'session_declined': "Sorry Your request was denied, please contact @{username} for more information",
    'session_confirmed': "✅ Your session request with @{username} has been confirmed.",
    'session_feedback': "💬 You have received feedback from @{username}.",
    'payment_confirmed': "💰 Payment confirmed for your session with @{username}.",
    'upcoming_session': "⏰ Reminder: You have an upcoming session with @{username} tomorrow.",
    'one_hr_session_reminder': "⏳ Reminder: Your session with @{username} starts in 1 hour.",
    'five_min_session_reminder': "⚡ Reminder: Your session with @{username} starts in 5 minutes.",
    'tutor_match': "🎯 We found a new tutor that matches your preferences — @{username}.",
    'important_announcement': "📢 Dear {recipient}, your account has been verified successfully.",
    'session_started': "📢 session with {username} just started",
    'session_ended': "📢 session with {username} just ended",
    'feedback_reminder': "📝 Don’t forget to share your experience by leaving feedback.",
    'session_started': "📝 Your session with @{username} has started",
    'session_ended': "📝 Your session with @{username} has completed",
}


def create_notification(recipient, user=None, type=None, link=None):
    """
    Creates both an in-app notification and a Telegram message if available.
    recipient: the user receiving the notification
    user: related user (tutor/student)
    type: notification type key
    link: optional redirect URL
    """
    if not type:
        return

    template = NOTIFICATION_MESSAGES.get(type)
    if not template:
        print(f"⚠️ Unknown notification type: {type}")
        return
    username = user.username if user else recipient.username
    message = template.format(username=username, recipient=recipient.username)

    # Save in-app notification
    Notification.objects.create(recipient=recipient, message=message, link=link)

    # Send Telegram message (optional)
    send_telegram_message(getattr(recipient, 'telegram_id', None), message)


    print(f"📨 Notification sent to {recipient.username}: {message}")
