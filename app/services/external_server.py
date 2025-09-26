import httpx
from app.core.config import settings

from app.log.logger_config import setup_logging

logger = setup_logging(__name__)

async def send_to_server(chat_id: str, user_input: str):
    payload = {
        "chat_id": chat_id,
        "user_input": user_input
    }
    
    timeout = settings.request_timeout
    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.post(
            str(settings.server_dest_url), 
            json=payload
        )
        resp.raise_for_status()
        resp = resp.json()
        logger.info(f"Sent to server: {payload}, received status: {resp}")
        
        return resp
