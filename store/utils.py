# store/utils.py
import requests
from django.conf import settings


def send_telegram_message(chat_id, message):
    token = settings.TELEGRAM_BOT_TOKEN
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}

    response = requests.post(url, data=payload)
    data = response.json()

    if not data.get("ok"):
        print(f"❌ Ошибка Telegram: {data}")
        return False

    return True

