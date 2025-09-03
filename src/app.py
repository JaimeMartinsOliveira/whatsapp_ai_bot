from fastapi import FastAPI, Request
import logging
from src.message_buffer import buffer_message

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request):
    try:
        payload = await request.json()
        logger.info(f"Webhook recebido: {payload}")
        if payload.get("event") == "messages.upsert":
            data = payload.get("data")
            if data and isinstance(data, dict):
                chat_id = data.get("key", {}).get("remoteJid")
                message = data.get("message", {}).get("conversation")
                if chat_id and message and not chat_id.endswith("@g.us"):
                    logger.info(f"Processando mensagem de {chat_id}")
                    await buffer_message(chat_id=chat_id, message=message)
        elif "data" in payload and isinstance(payload["data"], list):
            logger.info(f"Evento do tipo lista recebido ({payload.get('event')}), ignorando.")
        else:
            logger.warning(f"Evento não tratado: {payload.get('event')}")
    except Exception as e:
        logger.error(f"Erro ao processar webhook: {e}", exc_info=True)
    return {"status": "ok"}