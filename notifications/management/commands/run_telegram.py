from django.core.management.base import BaseCommand
import logging
from ...views import run_telegram_bot

class Command(BaseCommand):
    help = "Run telegram bot server"

    def handle(self, *args, **options):
        logging.info("📡 Telegram bot thread started.")
        run_telegram_bot()