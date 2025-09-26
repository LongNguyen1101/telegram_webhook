from telegram import Bot
from .config import settings
from telegram.ext import Application

from app.log.logger_config import setup_logging

logger = setup_logging(__name__)

bot = Bot(token=settings.telegram_token)
app_ptb = Application.builder().token(settings.telegram_token).build()

async def send_message(chat_id: int, text: str):
    logger.info(f"Sending message to chat_id {chat_id}: {text}")
    return await bot.send_message(chat_id=chat_id, text=text)
