# notifications/telegram_bot.py
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from django.conf import settings
from users.models import User

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    chat_id = update.effective_chat.id
    user_id = args[0] if args else None

    if not user_id:
        await update.message.reply_text("👋 Hi there! Please link your account from the HomeTutor website.")
        return

    try:
        user = User.objects.get(id=user_id)
        user.telegram_chat_id = chat_id
        user.save()
        await update.message.reply_text("✅ Your HomeTutor account is now linked to Telegram!")
    except User.DoesNotExist:
        await update.message.reply_text("⚠️ User not found. Please ensure you used the correct link.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I’ll send you tutoring updates, session reminders, and feedback alerts.")

def run_telegram_bot():
    """Starts the Telegram bot polling loop."""
    app = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    logging.info("🤖 Telegram bot is now polling...")
    app.run_polling()
