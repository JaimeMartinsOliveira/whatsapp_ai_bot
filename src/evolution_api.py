import requests
import logging
from src.config import (
    EVOLUTION_API_URL,
    EVOLUTION_INSTANCE_NAME,
    EVOLUTION_AUTHENTICATION_API_KEY,
)

logger = logging.getLogger(__name__)

def format_number(chat_id: str) -> str:
    return chat_id.split('@')[0]

def send_whatsapp_message(number: str, text: str):
    if not all([EVOLUTION_API_URL, EVOLUTION_INSTANCE_NAME, EVOLUTION_AUTHENTICATION_API_KEY]):
        logger.error("Variáveis de ambiente da Evolution API não estão configuradas.")
        return None
    url = f"{EVOLUTION_API_URL}/message/sendText/{EVOLUTION_INSTANCE_NAME}"
    headers = {
        "apikey": EVOLUTION_AUTHENTICATION_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {"number": number, "text": text}
    logger.info(f"Enviando para URL: {url} com Payload: {payload}")
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=20)
        logger.info(f"Evolution API Status: {response.status_code}")
        logger.info(f"Evolution API Response Body: {response.text}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro CRÍTICO na requisição para Evolution API: {e}", exc_info=True)
        return None