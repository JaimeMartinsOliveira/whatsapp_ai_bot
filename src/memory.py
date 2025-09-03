from langchain_community.chat_message_histories import RedisChatMessageHistory
from src.config import REDIS_URL

def get_session_history(session_id: str):
    return RedisChatMessageHistory(session_id=session_id, url=REDIS_URL)