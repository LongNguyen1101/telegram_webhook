from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from app.api.telegram_webhook import router as tg_router
from app.api.callback_webhook import router as cb_router
from app.core.config import settings
from app.core.bot_client import bot, app_ptb

app = FastAPI()
app.include_router(tg_router)
app.include_router(cb_router)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # đăng webhook
    webhook_url = f"{settings.webhook_base_url}/telegram/{settings.callback_secret}"
    await bot.setWebhook(webhook_url)

    # **Initialize** application trước khi start
    await app_ptb.initialize()

    # sau đó start
    await app_ptb.start()
    try:
        yield
    finally:
        await app_ptb.stop()

app = FastAPI(lifespan=lifespan)
app.include_router(tg_router)
app.include_router(cb_router)
