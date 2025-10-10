import traceback
from .config import settings
from telegram import Bot, constants
from telegram.ext import Application, ApplicationBuilder

from app.log.logger_config import setup_logging

logger = setup_logging(__name__)

bot = Bot(token=settings.telegram_token)
app_ptb = ApplicationBuilder().token(settings.telegram_token).build()
# app_ptb = Application.builder().token(settings.telegram_token).build()

async def send_message(chat_id: int, text: str):
    try:
        logger.info(f"Sending message to chat_id {chat_id}: {str(text)}")
        
        return await bot.send_message(
            chat_id=chat_id, 
            text=text, 
            parse_mode=constants.ParseMode.MARKDOWN
        )
        
    except Exception as e:
        error_details = traceback.format_exc()
        logger.error(f"Exception: {e}")
        logger.error(f"Chi tiết lỗi: \n{error_details}")
        raise
