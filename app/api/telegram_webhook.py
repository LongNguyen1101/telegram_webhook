import traceback
from telegram import Update
from app.core.config import settings
from app.core.bot_client import app_ptb, send_message
from app.services.external_server import send_to_server
from fastapi import APIRouter, Request, HTTPException, status

from app.log.logger_config import setup_logging

logger = setup_logging(__name__)

router = APIRouter()

@router.post("/telegram/{secret}")
@router.post("//telegram/{secret}")
async def telegram_webhook(secret: str, request: Request):
    if secret != settings.callback_secret:
        logger.error("Invalid secret in Telegram webhook")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    body = await request.json()
    update = Update.de_json(body, app_ptb.bot)

    chat = update.effective_chat
    msg = update.effective_message
    
    if chat is None or msg is None:
        logger.error("No chat or message in the update")
        return {"ok": False, "error": "no chat/message"}

    chat_id = str(chat.id)
    text = msg.text or ""

    try:
        logger.info(f"Received message from chat_id {chat_id}: {text}")
        await send_to_server(chat_id, text)
    except Exception as e:
        error_details = traceback.format_exc()
        logger.error(f"Exception: {e}")
        logger.error(f"Chi tiết lỗi: \n{error_details}")
        
        await send_message(chat_id, f"Đã có lỗi khi gửi xử lý: {e}")
        return {"ok": False, "error": str(e)}

    return {"ok": True}
