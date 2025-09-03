import asyncio
import logging
from collections import defaultdict
from src.evolution_api import send_whatsapp_message, format_number
from src.config import DEBOUNCE_SECONDS
from src.rag_chain import get_conversational_rag_chain

logger = logging.getLogger(__name__)
rag_chain_instance = get_conversational_rag_chain()
debounce_tasks = defaultdict(asyncio.Task)

async def buffer_message(chat_id: str, message: str):
    logger.info(f"Mensagem de {chat_id} agendada para processamento.")
    if debounce_tasks.get(chat_id):
        debounce_tasks[chat_id].cancel()
    debounce_tasks[chat_id] = asyncio.create_task(handle_debounce(chat_id, message))

async def handle_debounce(chat_id: str, original_message: str):
    try:
        await asyncio.sleep(float(DEBOUNCE_SECONDS))
        logger.info(f"Processando mensagem de {chat_id} com RAG: '{original_message}'")
        response_data = await rag_chain_instance.ainvoke(
            {"input": original_message},
            config={"configurable": {"session_id": chat_id}},
        )
        response_text = response_data.get("answer", "Desculpe, não consegui processar sua resposta.")
        send_whatsapp_message(
            number=format_number(chat_id),
            text=response_text
        )
        logger.info(f"Resposta enviada para {chat_id}: {response_text}")
    except asyncio.CancelledError:
        logger.warning(f"Envio cancelado para {chat_id}")
    except Exception as e:
        logger.error(f"ERRO CRÍTICO no handle_debounce para {chat_id}: {e}", exc_info=True)