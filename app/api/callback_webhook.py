from app.core.config import settings
from app.core.bot_client import send_message
from fastapi import APIRouter, Request, HTTPException, status

from app.log.logger_config import setup_logging

logger = setup_logging(__name__)

router = APIRouter()

@router.post("/callback/{secret}")
async def callback_webhook(secret: str, request: Request):
    if secret != settings.callback_secret:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    data = await request.json()
    chat_id = data.get("chat_id")
    response = data.get("response")

    if chat_id is None or response is None:
        logger.error("Nothing to process, missing chat_id or response")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Missing chat_id or content"
        )
    
    if response["error"]:
        logger.error(f"Error from external server: {response['error']}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=response["error"]
        )

    logger.info(f"Received callback for chat_id {chat_id}")

    # gửi kết quả về người dùng
    await send_message(chat_id=chat_id, text=response["content"])
    return {"status": "ok"}
