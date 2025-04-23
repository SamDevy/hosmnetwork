# utils/telegram_sender.py

import aiohttp
import logging

logger = logging.getLogger(__name__)

async def send_telegram_message(bot_token: str, chat_id: str, message: str):
    """
    Sends a message to a Telegram bot using async HTTP request.
    Requires:
    - bot_token: Your Telegram bot token
    - chat_id: The ID of the chat or channel
    - message: The text you want to send
    """
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=payload) as response:
                if response.status != 200:
                    text = await response.text()
                    logger.error(f"Error sending message: {text}")
    except Exception as e:
        logger.exception(f"Exception in send_telegram_message: {e}")
