# notifications/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,  get_object_or_404
from .models import Notification
import logging
from asgiref.sync import sync_to_async
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from users.models import User

@login_required
def notification_list(request):
    notifications = request.user.notifications.all()
    return render(request, 'notification/notifications.html', {'notifications': notifications})

@login_required
def mark_notification_read(request, notif_id):
    notif = get_object_or_404(Notification, id=notif_id, recipient=request.user)
    notif.mark_as_read()
    return redirect(notif.link or 'notification_list')


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    chat_id = update.effective_chat.id

    if not args:
        await update.message.reply_text("👋 Hello! Please connect your account from the website.")
        return

    user_id = args[0]

    try:
        user = await sync_to_async(User.objects.get)(id=user_id)
        user.telegram_id = chat_id
        user = user.username
        await sync_to_async(user.save)()
        await update.message.reply_text(f'✅ Hi ${user} Your Telegram account is now linked successfully!')
    except User.DoesNotExist:
        await update.message.reply_text("❌ Invalid user ID. Please try linking again from the website.")


def run_telegram_bot():
    application = ApplicationBuilder().token("7564093391:AAGJYuuFGFnedl2k73XOfyPNI93VmjqASjs").build()
    application.add_handler(CommandHandler("start", start))
    logging.info("🚀 Telegram bot started and polling...")
    application.run_polling()